"""Visualization charts for SHAP explanations."""

import os
import matplotlib.pyplot as plt
import pandas as pd
import shap
from pathlib import Path

# Use Agg backend for headless environments
plt.switch_backend('Agg')

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EVAL_DIR = PROJECT_ROOT / "xai" / "evaluation"
EVAL_DIR.mkdir(parents=True, exist_ok=True)

def generate_summary_plot(explainer: shap.TreeExplainer, X: pd.DataFrame, max_display: int = 10):
    """Generate and save the SHAP summary dot plot."""
    from xai.explainer import get_shap_values
    phishing_shap, _ = get_shap_values(X)

    plt.figure(figsize=(10, 8))
    shap.summary_plot(phishing_shap, X, show=False, max_display=max_display)
    plt.tight_layout()
    plt.savefig(EVAL_DIR / "shap_summary.png", dpi=300, bbox_inches='tight')
    plt.close()


def generate_bar_chart(explainer: shap.TreeExplainer, X: pd.DataFrame, max_display: int = 10):
    """Generate and save the SHAP feature importance bar chart."""
    from xai.explainer import get_shap_values
    phishing_shap, _ = get_shap_values(X)
        
    plt.figure(figsize=(10, 8))
    shap.summary_plot(phishing_shap, X, plot_type="bar", show=False, max_display=max_display)
    plt.tight_layout()
    plt.savefig(EVAL_DIR / "bar_chart.png", dpi=300, bbox_inches='tight')
    plt.close()


def generate_waterfall_plot(explainer: shap.TreeExplainer, X: pd.DataFrame, row_index: int = 0):
    """Generate and save a SHAP waterfall plot for a single prediction."""
    # Waterfall plot requires an Explanation object
    explanation = explainer(X)
    
    # explanation object shape: (rows, features, classes) or (rows, features)
    if len(explanation.shape) == 3:
        # Binary classification
        exp = explanation[row_index, :, 1]
    else:
        exp = explanation[row_index]

    plt.figure(figsize=(10, 8))
    shap.plots.waterfall(exp, show=False)
    plt.tight_layout()
    plt.savefig(EVAL_DIR / "waterfall.png", dpi=300, bbox_inches='tight')
    plt.close()
