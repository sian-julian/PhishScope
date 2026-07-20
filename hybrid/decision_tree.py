"""Decision tree logic for the Hybrid Detection Engine."""

def apply_rules(heuristic_verdict: str, ml_prediction: str, confidence: str) -> tuple[str | None, str | None, list[str]]:
    """
    Apply hardcoded override rules.
    Returns (override_verdict, override_confidence, reasons).
    If no rule matched, returns (None, None, []).
    """
    reasons = []
    
    if heuristic_verdict == "DANGEROUS" and ml_prediction == "PHISHING":
        reasons.append("Both heuristic and ML engines strongly indicate phishing.")
        return "DANGEROUS", "VERY_HIGH", reasons
        
    if heuristic_verdict == "SAFE" and ml_prediction == "SAFE":
        reasons.append("Both engines indicate the URL is safe.")
        return "SAFE", "HIGH", reasons
        
    if heuristic_verdict == "SAFE" and ml_prediction == "PHISHING":
        reasons.append("ML model identified phishing despite safe heuristics.")
        return "SUSPICIOUS", "MEDIUM", reasons
        
    if heuristic_verdict == "DANGEROUS" and ml_prediction == "SAFE":
        reasons.append("Heuristic flagged as dangerous despite safe ML prediction.")
        return "SUSPICIOUS", "MEDIUM", reasons
        
    if heuristic_verdict == "SUSPICIOUS" and ml_prediction == "PHISHING":
        reasons.append("Suspicious heuristics corroborated by ML phishing prediction.")
        return "DANGEROUS", "HIGH", reasons

    return None, None, []
