"""Hybrid Detection Engine orchestrator."""

import sys
from pathlib import Path
from time import perf_counter
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from backend.analyzer.feature_extractor import extract_features
    from backend.analyzer.scoring_engine import score_url
    from backend.config import logger
    from ml.scripts.predict import predict_url
except ImportError:
    from analyzer.feature_extractor import extract_features
    from analyzer.scoring_engine import score_url
    from config import logger
    from ml.scripts.predict import predict_url

from hybrid.confidence import calculate_confidence
from hybrid.decision_tree import apply_rules
from hybrid.utils import build_hybrid_response, calculate_hybrid_score, get_hybrid_verdict


def analyze_url(url: str, benchmark: bool = False) -> dict[str, Any]:
    """
    End-to-end analysis combining heuristic and ML layers into a hybrid verdict.
    """
    start_time = perf_counter()
    logger.info("Starting Hybrid Engine for: %s", url)

    # 1. Feature Extraction & Heuristic Scoring (Phase 2)
    features = extract_features(url)
    if not features.get("valid"):
        logger.warning("Invalid URL received by hybrid engine: %s", url)
        return {"error": "Invalid URL"}

    heuristic_result = score_url(features, benchmark=False)
    
    # Clean heuristic metadata if it exists (score_url might return execution_time_ms)
    heuristic_meta = {}
    if "execution_time_ms" in heuristic_result:
        heuristic_meta["execution_time_ms"] = heuristic_result.pop("execution_time_ms")

    heuristic_score = heuristic_result.get("score", 0)
    heuristic_verdict = heuristic_result.get("verdict", "SAFE")

    # 2. ML Prediction (Phase 5)
    ml_result = predict_url(url, features=features)
    ml_prediction = ml_result.get("prediction", "SAFE")
    ml_prob = ml_result.get("confidence", 0.0)
    if ml_prediction == "SAFE":
        # We need the probability of PHISHING for the score. 
        # If the model gives confidence of being SAFE, the phish prob is (1 - confidence)
        phishing_prob = 1.0 - ml_prob
    elif ml_prediction == "PHISHING":
        phishing_prob = ml_prob
    else:
        # Error or unexpected
        phishing_prob = 0.0
        ml_prediction = "ERROR"

    # 3. Hybrid Engine Consensus
    base_confidence = calculate_confidence(phishing_prob)
    hybrid_score = calculate_hybrid_score(heuristic_score, phishing_prob)
    default_verdict = get_hybrid_verdict(hybrid_score)
    
    # 4. Apply Decision Rules
    override_verdict, override_confidence, reasons = apply_rules(
        heuristic_verdict, ml_prediction, base_confidence
    )
    
    final_verdict = override_verdict if override_verdict else default_verdict
    final_confidence = override_confidence if override_confidence else base_confidence

    if not reasons:
        reasons.append("Hybrid engine consensus reached.")
        
    if ml_prob > 0.95:
        reasons.append(f"Random Forest confidence exceeded 95%.")

    logger.info("Heuristic: %s", heuristic_verdict)
    logger.info("ML: %s", ml_prediction)
    logger.info("Hybrid: %s", final_verdict)

    result = build_hybrid_response(
        heuristic=heuristic_result,
        ml=ml_result,
        hybrid_score=hybrid_score,
        hybrid_verdict=final_verdict,
        hybrid_confidence=final_confidence,
        reasons=reasons
    )

    if benchmark:
        execution_time = (perf_counter() - start_time) * 1000
        result["hybrid"]["execution_time_ms"] = round(execution_time, 2)
        if execution_time > 50:
            logger.warning("Hybrid execution took >50ms (%.2fms)", execution_time)

    return result
