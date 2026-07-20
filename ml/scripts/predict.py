"""Prediction pipeline for Phase 5 Machine Learning layer."""

import sys
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.analyzer.feature_extractor import extract_features
from datasets.scripts.build_features import _feature_row
from ml.scripts.common import MODELS_DIR, logger
from ml.scripts.train import NON_FEATURE_COLS

_MODEL_CACHE = None


def _load_model() -> Any:
    """Load model from disk, using cache if available."""
    global _MODEL_CACHE
    if _MODEL_CACHE is not None:
        return _MODEL_CACHE

    model_path = MODELS_DIR / "best_model.pkl"
    if not model_path.exists():
        model_path = MODELS_DIR / "random_forest.pkl"
        if not model_path.exists():
            raise FileNotFoundError("No trained model found in ml/models/")

    _MODEL_CACHE = joblib.load(model_path)
    return _MODEL_CACHE


def _prepare_features(url: str, features: dict[str, Any] | None = None) -> pd.DataFrame:
    """Extract features and prepare DataFrame for prediction."""
    if features is None:
        features = extract_features(url)
        
    if not features.get("valid"):
        raise ValueError(f"Invalid URL: {url}")
        
    row_dict = _feature_row(url, label=0, source="predict", features=features)
    
    # Drop non-feature columns
    drop_cols = [col for col in NON_FEATURE_COLS if col in row_dict]
    for col in drop_cols:
        row_dict.pop(col, None)
        
    # Build dataframe
    # Ensuring order is maintained as per extraction
    return pd.DataFrame([row_dict])


def predict_url(url: str, features: dict[str, Any] | None = None) -> dict[str, Any]:
    """Predict whether a URL is phishing or safe."""
    try:
        model = _load_model()
        X = _prepare_features(url, features=features)
        
        prediction = model.predict(X)[0]
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(X)[0]
            confidence = probabilities[1] if prediction == 1 else probabilities[0]
        else:
            confidence = 1.0  # Fallback for models without predict_proba

        verdict = "PHISHING" if prediction == 1 else "SAFE"
        
        return {
            "prediction": verdict,
            "confidence": round(float(confidence), 4)
        }
    except Exception as e:
        logger.error("Prediction failed for %s: %s", url, e)
        return {
            "prediction": "ERROR",
            "confidence": 0.0,
            "error": str(e)
        }


def predict_batch(urls: list[str]) -> list[dict[str, Any]]:
    """Predict a batch of URLs."""
    results = []
    for url in urls:
        results.append(predict_url(url))
    return results

