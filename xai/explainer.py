"""SHAP Explainer wrapper for the ML Model."""

import sys
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
import shap

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.scripts.common import MODELS_DIR, logger

_EXPLAINER_CACHE = None
_MODEL_CACHE = None

def _load_model() -> Any:
    """Load the model for the explainer."""
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

def get_explainer() -> shap.TreeExplainer:
    """Get or initialize the SHAP TreeExplainer."""
    global _EXPLAINER_CACHE
    if _EXPLAINER_CACHE is not None:
        return _EXPLAINER_CACHE

    model = _load_model()
    # SHAP requires the actual model, not pipelines. 
    # Luckily, our best_model.pkl is just the classifier itself.
    _EXPLAINER_CACHE = shap.TreeExplainer(model)
    return _EXPLAINER_CACHE

def get_shap_values(X: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """
    Calculate SHAP values for the input feature vector.
    Returns (shap_values_for_phishing_class, expected_value).
    """
    try:
        explainer = get_explainer()
        # explainer.shap_values(X) returns a list of arrays for classification models, 
        # where list[1] is the positive class (PHISHING = 1).
        # We disable check_additivity to drastically improve batch performance.
        shap_values = explainer.shap_values(X, check_additivity=False)
        
        if isinstance(shap_values, list):
            # Binary classification (SAFE vs PHISHING) returning list of 2D
            phishing_shap = shap_values[1]
            base_value = explainer.expected_value[1]
        elif len(shap_values.shape) == 3:
            # Binary classification returning 3D array (N, features, classes)
            phishing_shap = shap_values[:, :, 1]
            base_value = explainer.expected_value[1]
        else:
            # Single array depending on model type
            phishing_shap = shap_values
            base_value = explainer.expected_value
            
        return phishing_shap, base_value
    except Exception as e:
        logger.error("Failed to generate SHAP values: %s", e)
        raise
