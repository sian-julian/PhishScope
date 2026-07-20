"""Generate accuracy comparison for Heuristic vs ML vs Hybrid."""

import sys
from pathlib import Path
from time import perf_counter

import pandas as pd
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from backend.analyzer.feature_extractor import extract_features
    from backend.analyzer.scoring_engine import score_url
    from ml.scripts.predict import predict_url
    from hybrid.engine import analyze_url
except ImportError:
    from analyzer.feature_extractor import extract_features
    from analyzer.scoring_engine import score_url
    from ml.scripts.predict import predict_url
    from hybrid.engine import analyze_url

from ml.scripts.common import TEST_PATH
from backend.config import logger


def _process_url(row):
    url = row.url
    actual_label = "PHISHING" if row.label == 1 else "SAFE"
    result = analyze_url(url, benchmark=False)
    
    if "error" in result:
        return None
        
    h_verdict = result["heuristic"]["verdict"]
    h_binary = "PHISHING" if h_verdict in ["PHISHING", "DANGEROUS", "SUSPICIOUS"] else "SAFE"
    
    m_verdict = result["ml"]["prediction"]
    
    hy_verdict = result["hybrid"]["verdict"]
    hy_binary = "PHISHING" if hy_verdict in ["PHISHING", "DANGEROUS", "SUSPICIOUS"] else "SAFE"
    
    return {
        "h_correct": 1 if h_binary == actual_label else 0,
        "m_correct": 1 if m_verdict == actual_label else 0,
        "hy_correct": 1 if hy_binary == actual_label else 0
    }

def generate_accuracy_comparison():
    """Run engines over the test dataset and compare accuracy."""
    logger.info("Loading test dataset for comparison: %s", TEST_PATH)
    import logging
    logger.setLevel(logging.WARNING)
    
    df = pd.read_csv(TEST_PATH)
    
    # Sample 1000 URLs for rapid evaluation since feature extraction is non-vectorized
    df = df.sample(n=1000, random_state=42)
    
    heuristic_correct = 0
    ml_correct = 0
    hybrid_correct = 0
    total = len(df)
    
    start_time = perf_counter()
    
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=8) as executor:
        # Convert itertuples to a list of dicts to avoid any namedtuple issues, although ThreadPool doesn't pickle.
        rows = [row for row in df.itertuples(index=False)]
        results = list(tqdm(executor.map(_process_url, rows), total=total, desc="Comparing Engines"))
        
    for res in results:
        if res:
            heuristic_correct += res["h_correct"]
            ml_correct += res["m_correct"]
            hybrid_correct += res["hy_correct"]
            
    execution_time = perf_counter() - start_time
    
    heuristic_acc = round((heuristic_correct / total) * 100, 2)
    ml_acc = round((ml_correct / total) * 100, 2)
    hybrid_acc = round((hybrid_correct / total) * 100, 2)
    
    res_dicts = [
        {"Engine": "Heuristic", "Accuracy": heuristic_acc},
        {"Engine": "Random Forest", "Accuracy": ml_acc},
        {"Engine": "Hybrid", "Accuracy": hybrid_acc},
    ]
    
    results_df = pd.DataFrame(res_dicts)
    
    eval_dir = PROJECT_ROOT / "hybrid" / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)
    out_path = eval_dir / "accuracy_comparison.csv"
    
    results_df.to_csv(out_path, index=False)
    
    print(f"Evaluation completed in {execution_time:.2f}s")
    print(results_df.to_string(index=False))

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    generate_accuracy_comparison()
