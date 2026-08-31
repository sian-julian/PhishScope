"""Text formatter for XAI explanations."""

from xai.utils import get_readable_feature_name
from xai.human_explanations import get_human_explanation

def format_explanation(verdict: str, top_features: list[dict], level: int = 3) -> dict:
    """
    Format SHAP explanations into human-readable structures.
    """
    if verdict == "SAFE":
        summary = "This URL was classified as safe because no major phishing indicators were detected."
    elif verdict == "SUSPICIOUS":
        summary = "This URL appears suspicious."
        if level >= 2:
            summary = "The model identified several suspicious indicators."
    else:
        summary = "This URL appears suspicious."
        if level >= 2:
            summary = "The model identified several phishing indicators."
            
    # Format top features array for JSON response
    formatted_features = []
    positive_indicators = []
    seen_texts = set()
    
    for feat in top_features:
        name = feat["name"]
        impact = feat["importance"]
        readable_name = get_readable_feature_name(name)
        human_text = get_human_explanation(name, level="BASIC")
        
        if human_text in seen_texts:
            continue
        seen_texts.add(human_text)
        
        impact_pct = f"{'+' if impact > 0 else ''}{int(round(impact * 100))}%"
        
        formatted_features.append({
            "feature": human_text,
            "impact": impact_pct
        })
        
        if impact > 0:
            positive_indicators.append(readable_name)

    # Build advanced summary if level >= 3 and there are positive indicators
    if level >= 3 and verdict in ["PHISHING", "DANGEROUS"] and positive_indicators:
        if len(positive_indicators) == 1:
            summary = f"This URL was classified as phishing primarily due to {positive_indicators[0].lower()}."
        elif len(positive_indicators) == 2:
            summary = f"This URL was classified as phishing primarily due to a {positive_indicators[0].lower()} and a {positive_indicators[1].lower()}."
        else:
            summary = f"This URL was classified as phishing primarily due to a {positive_indicators[0].lower()}, a {positive_indicators[1].lower()}, and other factors."

    return {
        "summary": summary,
        "top_features": formatted_features
    }
