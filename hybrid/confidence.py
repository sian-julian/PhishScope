"""Confidence analysis for the Hybrid Detection Engine."""

def calculate_confidence(probability: float) -> str:
    """Calculate a categorical confidence level based on ML probability."""
    if not isinstance(probability, (int, float)):
        return "LOW"
        
    if probability > 0.95:
        return "VERY_HIGH"
    elif probability > 0.85:
        return "HIGH"
    elif probability > 0.70:
        return "MEDIUM"
    else:
        return "LOW"
