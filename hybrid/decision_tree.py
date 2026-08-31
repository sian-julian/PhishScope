"""Decision tree logic for the Hybrid Detection Engine."""

def apply_rules(heuristic_verdict: str, ml_prediction: str, confidence: str, heuristic_score: int = 0) -> tuple[str | None, str | None, list[str]]:
    """
    Apply hardcoded override rules.
    Returns (override_verdict, override_confidence, reasons).
    If no rule matched, returns (None, None, []).
    
    The heuristic_score parameter allows this function to distinguish between
    "heuristic says SAFE with zero evidence" vs "heuristic says SAFE with some
    minor indicators that didn't cross the threshold."
    """
    reasons = []
    
    if heuristic_verdict == "DANGEROUS" and ml_prediction == "PHISHING":
        reasons.append("Both heuristic and ML engines strongly indicate phishing.")
        return "DANGEROUS", "VERY_HIGH", reasons
        
    if heuristic_verdict == "SAFE" and ml_prediction == "SAFE":
        reasons.append("Both engines indicate the URL is safe.")
        return "SAFE", "HIGH", reasons
        
    if heuristic_verdict == "SAFE" and ml_prediction == "PHISHING":
        if heuristic_score == 0:
            if confidence == "VERY_HIGH":
                reasons.append("ML model identified a strong phishing pattern despite no heuristic indicators.")
                return "SUSPICIOUS", "MEDIUM", reasons
            else:
                reasons.append("ML flagged as phishing but confidence is not maximal and no heuristic indicators found. Treating as safe.")
                return "SAFE", "MEDIUM", reasons
        else:
            reasons.append("ML model identified phishing with corroborating heuristic signals.")
            return "SUSPICIOUS", "MEDIUM", reasons
        
    if heuristic_verdict == "DANGEROUS" and ml_prediction == "SAFE":
        reasons.append("Heuristic flagged as dangerous despite safe ML prediction.")
        return "SUSPICIOUS", "MEDIUM", reasons
        
    if heuristic_verdict == "SUSPICIOUS" and ml_prediction == "PHISHING":
        reasons.append("Suspicious heuristics corroborated by ML phishing prediction.")
        return "DANGEROUS", "HIGH", reasons

    return None, None, []
