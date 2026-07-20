"""Evaluate SHAP explanations and generate charts."""

import sys
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from ml.scripts.common import TEST_PATH, logger
    from ml.scripts.train import NON_FEATURE_COLS
    from xai.explainer import get_explainer, get_shap_values
    from xai.charts import generate_summary_plot, generate_bar_chart, generate_waterfall_plot
except ImportError:
    from ml.scripts.common import TEST_PATH, logger
    from ml.scripts.train import NON_FEATURE_COLS
    from xai.explainer import get_explainer, get_shap_values
    from xai.charts import generate_summary_plot, generate_bar_chart, generate_waterfall_plot

EVAL_DIR = PROJECT_ROOT / "xai" / "evaluation"

def evaluate_xai():
    """Run SHAP evaluation over a sample of the test dataset."""
    logger.info("Loading test dataset: %s", TEST_PATH)
    df = pd.read_csv(TEST_PATH)
    
    # We drop non-feature cols to get the raw X matrix
    drop_cols = [col for col in NON_FEATURE_COLS if col in df.columns]
    X_full = df.drop(columns=drop_cols)
    
    # Sample 100 URLs for performance benchmarking
    X_sample = X_full.sample(n=100, random_state=42)
    
    logger.info("Benchmarking SHAP explanation generation for 100 URLs...")
    start_time = perf_counter()
    
    # Force initialize cache
    explainer = get_explainer()
    
    # Generate for all 100 at once (batch mode)
    shap_values_batch, _ = get_shap_values(X_sample)
    
    batch_time = perf_counter() - start_time
    logger.info("Batch generation (100 URLs): %.2fs", batch_time)
    
    # Single URL timing
    single_start = perf_counter()
    _ = get_shap_values(X_sample.iloc[[0]])
    single_time = (perf_counter() - single_start) * 1000
    logger.info("Single generation: %.2fms", single_time)
    
    # Build feature ranking
    logger.info("Generating feature ranking CSV...")
    # Get mean absolute SHAP value per feature
    mean_abs_shap = np.abs(shap_values_batch).mean(axis=0)
    features = list(X_sample.columns)
    
    ranking = []
    for i, feat in enumerate(features):
        ranking.append({
            "Feature": feat,
            "Importance": round(mean_abs_shap[i], 4)
        })
        
    ranking.sort(key=lambda x: x["Importance"], reverse=True)
    ranking_df = pd.DataFrame(ranking)
    ranking_df.to_csv(EVAL_DIR / "feature_ranking.csv", index=False)
    
    # Save metrics
    metrics = {
        "Single URL Time (ms)": round(single_time, 2),
        "Batch 100 URLs Time (s)": round(batch_time, 2),
        "Top Feature": ranking[0]["Feature"] if ranking else "N/A"
    }
    pd.DataFrame([metrics]).to_csv(EVAL_DIR / "metrics.csv", index=False)
    
    # Generate charts
    logger.info("Generating SHAP charts...")
    # Use the 100 sample for summary/bar to keep it readable and fast
    generate_summary_plot(explainer, X_sample)
    generate_bar_chart(explainer, X_sample)
    
    # Waterfall for a single clear phishing prediction
    phishing_indices = df[df["label"] == 1].index
    if not phishing_indices.empty:
        idx = phishing_indices[0]
        X_phish = X_full.iloc[[idx]]
        generate_waterfall_plot(explainer, X_phish, row_index=0)
    else:
        generate_waterfall_plot(explainer, X_sample, row_index=0)
        
    logger.info("XAI evaluation complete.")

if __name__ == "__main__":
    evaluate_xai()
