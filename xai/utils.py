"""Utility functions for SHAP integration."""

import numpy as np

# Map model feature names to human-readable format
FEATURE_NAMES = {
    "url_length": "URL Length",
    "url_length_risk_points": "URL Length Risk",
    "subdomains": "Number of Subdomains",
    "dot_count": "Excessive Dots",
    "hyphen_count": "Excessive Hyphens",
    "at_count": "At-Symbol (@) Usage",
    "token_count": "Token Count",
    "digit_ratio": "High Digit Ratio",
    "entropy": "High Entropy",
    "uses_https": "HTTPS Misuse",
    "tld_score": "Suspicious TLD",
    "brand_mismatch": "Brand Mismatch",
    "ascii_lookalike_detected": "Lookalike Domain"
}

def get_readable_feature_name(feature: str) -> str:
    """Get the human-readable string for a feature name."""
    return FEATURE_NAMES.get(feature, feature.replace("_", " ").title())

def get_top_features(
    shap_values: np.ndarray, 
    feature_names: list[str], 
    top_n: int = 3
) -> list[dict]:
    """
    Extract the top N contributing features from SHAP values.
    Returns a list of dicts with 'name' and 'importance' sorted by absolute impact.
    """
    # Create list of (feature, shap_value)
    contributions = []
    for i, val in enumerate(shap_values):
        contributions.append({
            "name": feature_names[i],
            "importance": float(val)
        })
        
    # Sort by absolute impact descending
    contributions.sort(key=lambda x: abs(x["importance"]), reverse=True)
    
    return contributions[:top_n]
