"""Text formatter for XAI explanations."""

from xai.utils import get_readable_feature_name

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
    
    for feat in top_features:
        name = feat["name"]
        impact = feat["importance"]
        readable_name = get_readable_feature_name(name)
        
        # Format the impact percentage string (e.g. "+24%")
        # SHAP values represent log odds in TreeExplainer, but for human readability
        # we often just scale them or show them directly. The prompt implies "+24%".
        # We will just multiply by 100 and add a sign.
        impact_pct = f"{'+' if impact > 0 else ''}{int(round(impact * 100))}%"
        
        formatted_features.append({
            "feature": name,
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
