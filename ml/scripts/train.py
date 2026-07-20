"""Train the Machine Learning model."""

import json
import sys
from pathlib import Path
from time import perf_counter
from typing import Any

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.scripts.common import (
    EVALUATION_DIR,
    MODELS_DIR,
    TRAIN_PATH,
    add_benchmark,
    logger,
    save_json,
)

NON_FEATURE_COLS = ["url", "source", "tld_risk_level", "brand_position", "lookalike_matched_brand", "label"]


def load_training_data(path: Path) -> tuple[pd.DataFrame, pd.Series]:
    """Load train.csv and return X and y."""
    if not path.exists():
        raise FileNotFoundError(f"Missing train data file: {path}")
    
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("Train dataset is empty")
    
    y = df["label"]
    drop_cols = [col for col in NON_FEATURE_COLS if col in df.columns]
    X = df.drop(columns=drop_cols)
    return X, y


def train_model(benchmark: bool = False) -> dict[str, Any]:
    """Train the model and save it."""
    start_time = perf_counter()
    logger.info("Training started.")
    
    X, y = load_training_data(TRAIN_PATH)
    
    model_name = "Random Forest"
    best_model = None
    
    if benchmark:
        logger.info("Running model benchmark comparison...")
        models = {
            "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42, n_jobs=-1),
            "Decision Tree": DecisionTreeClassifier(random_state=42),
            "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
            "SVM": SVC(kernel="linear", random_state=42)
        }
        
        results = []
        best_score = 0
        best_model_name = ""
        
        for name, clf in models.items():
            clf.fit(X, y)
            score = clf.score(X, y) * 100
            results.append({"Model": name, "Accuracy": score})
            if score > best_score:
                best_score = score
                best_model = clf
                best_model_name = name
                
        results_df = pd.DataFrame(results)
        eval_path = EVALUATION_DIR / "model_comparison.csv"
        results_df.to_csv(eval_path, index=False)
        logger.info("Model comparison saved to %s", eval_path)
        
        model_name = best_model_name
        model_to_save = best_model
        save_path = MODELS_DIR / "best_model.pkl"
    else:
        model_to_save = RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42, n_jobs=-1)
        model_to_save.fit(X, y)
        save_path = MODELS_DIR / "random_forest.pkl"

    joblib.dump(model_to_save, save_path)
    logger.info("Model saved to %s", save_path)
    
    training_time = perf_counter() - start_time
    metadata = {
        "model": model_name,
        "n_estimators": 100 if model_name == "Random Forest" else None,
        "training_rows": len(y),
        "training_time_seconds": round(training_time, 2)
    }
    
    meta_path = MODELS_DIR / "model_metadata.json"
    save_json(metadata, meta_path)
    
    stats = {
        "model_name": model_name,
        "training_rows": len(y),
        "output_model": str(save_path),
    }
    return add_benchmark(stats, benchmark, start_time)


if __name__ == "__main__":
    benchmark_flag = "--benchmark" in sys.argv
    train_model(benchmark=benchmark_flag)
