"""Utility functions for the Hybrid Detection Engine."""

def calculate_hybrid_score(heuristic_score: float, ml_probability: float) -> int:
    """
    Calculate the consensus hybrid score.
    Formula: (heuristic_score * 0.4) + (ml_probability * 100 * 0.6)
    """
    score = (heuristic_score * 0.4) + (ml_probability * 100 * 0.6)
    return int(round(score))

def get_hybrid_verdict(hybrid_score: int) -> str:
    """Determine the verdict based on hybrid score bands."""
    if hybrid_score <= 30:
        return "SAFE"
    elif hybrid_score <= 60:
        return "SUSPICIOUS"
    else:
        return "DANGEROUS"

def build_hybrid_response(
    heuristic: dict,
    ml: dict,
    hybrid_score: int,
    hybrid_verdict: str,
    hybrid_confidence: str,
    reasons: list[str]
) -> dict:
    """Format the final unified response."""
    return {
        "heuristic": heuristic,
        "ml": ml,
        "hybrid": {
            "score": hybrid_score,
            "verdict": hybrid_verdict,
            "confidence": hybrid_confidence,
            "reasons": reasons
        }
    }
