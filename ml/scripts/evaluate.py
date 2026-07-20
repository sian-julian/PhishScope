"""Evaluate the trained Machine Learning model."""

import json
import sys
from pathlib import Path
from time import perf_counter
from typing import Any

import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
    ConfusionMatrixDisplay,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.scripts.common import (
    EVALUATION_DIR,
    MODELS_DIR,
    TEST_PATH,
    add_benchmark,
    logger,
    save_json,
)
from ml.scripts.train import load_training_data


def evaluate_model(benchmark: bool = False) -> dict[str, Any]:
    """Load model, generate metrics and artifacts."""
    start_time = perf_counter()
    
    # Check for best_model.pkl first, then random_forest.pkl
    model_path = MODELS_DIR / "best_model.pkl"
    if not model_path.exists():
        model_path = MODELS_DIR / "random_forest.pkl"
        if not model_path.exists():
            raise FileNotFoundError("No trained model found.")

    model = joblib.load(model_path)
    X_test, y_test = load_training_data(TEST_PATH)
    
    predictions = model.predict(X_test)
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X_test)[:, 1]
    else:
        # For SVC without probability=True
        probabilities = predictions
        
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, zero_division=0)
    recall = recall_score(y_test, predictions, zero_division=0)
    f1 = f1_score(y_test, predictions, zero_division=0)
    
    try:
        roc_auc = roc_auc_score(y_test, probabilities)
    except ValueError:
        roc_auc = 0.0

    metrics = {
        "accuracy": round(accuracy * 100, 2),
        "precision": round(precision * 100, 2),
        "recall": round(recall * 100, 2),
        "f1_score": round(f1 * 100, 2),
        "roc_auc": round(roc_auc * 100, 2),
    }

    logger.info("Accuracy: %s%%", metrics["accuracy"])
    
    for metric_name, value in metrics.items():
        if value < 90.0:
            logger.warning("Warning: %s fell below 90%% (Value: %s%%)", metric_name, value)
            
    save_json(metrics, EVALUATION_DIR / "metrics.json")
    
    report = classification_report(y_test, predictions, target_names=["Safe", "Phishing"])
    with open(EVALUATION_DIR / "classification_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
        
    # Confusion Matrix
    cm = confusion_matrix(y_test, predictions)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Safe", "Phishing"])
    plt.switch_backend('Agg')
    fig, ax = plt.subplots()
    disp.plot(ax=ax, cmap="Blues")
    plt.title("Confusion Matrix")
    plt.savefig(EVALUATION_DIR / "confusion_matrix.png")
    plt.close()
    
    # ROC Curve
    if hasattr(model, "predict_proba"):
        fpr, tpr, _ = roc_curve(y_test, probabilities)
        plt.figure()
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic')
        plt.legend(loc="lower right")
        plt.savefig(EVALUATION_DIR / "roc_curve.png")
        plt.close()
        
    # Feature Importance
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        feature_names = X_test.columns
        fi_df = pd.DataFrame({"Feature": feature_names, "Importance": importances})
        fi_df = fi_df.sort_values(by="Importance", ascending=False)
        fi_df.to_csv(EVALUATION_DIR / "feature_importance.csv", index=False)
        
        top_features = fi_df.head(10)
        logger.info("Top Feature:\n%s", top_features.iloc[0]["Feature"])
        print("\nTop 10 Features:")
        print(top_features.to_string(index=False))
        
    stats = {
        "test_rows": len(y_test),
        "accuracy": metrics["accuracy"],
    }
    return add_benchmark(stats, benchmark, start_time)


if __name__ == "__main__":
    benchmark_flag = "--benchmark" in sys.argv
    evaluate_model(benchmark=benchmark_flag)
