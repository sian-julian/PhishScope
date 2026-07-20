"""Tests for Phase 7 XAI Integration."""

import numpy as np
import pandas as pd
import pytest

from xai.utils import get_readable_feature_name, get_top_features
from xai.formatter import format_explanation


def test_get_readable_feature_name():
    assert get_readable_feature_name("url_length") == "URL Length"
    assert get_readable_feature_name("tld_score") == "Suspicious TLD"
    assert get_readable_feature_name("unknown_feature") == "Unknown Feature"

def test_get_top_features():
    shap_vals = np.array([0.1, -0.5, 0.3, 0.05])
    features = ["feat1", "feat2", "feat3", "feat4"]
    
    top = get_top_features(shap_vals, features, top_n=2)
    assert len(top) == 2
    assert top[0]["name"] == "feat2"
    assert top[0]["importance"] == -0.5
    assert top[1]["name"] == "feat3"
    assert top[1]["importance"] == 0.3

def test_format_explanation_safe():
    res = format_explanation("SAFE", [])
    assert "safe" in res["summary"].lower()

def test_format_explanation_dangerous_level_1():
    res = format_explanation("DANGEROUS", [], level=1)
    assert res["summary"] == "This URL appears suspicious."

def test_format_explanation_dangerous_level_2():
    res = format_explanation("DANGEROUS", [], level=2)
    assert "indicators" in res["summary"].lower()

def test_format_explanation_dangerous_level_3():
    top_features = [
        {"name": "lookalike", "importance": 0.24},
        {"name": "entropy", "importance": 0.15}
    ]
    res = format_explanation("DANGEROUS", top_features, level=3)
    assert "primarily due to" in res["summary"]
    assert "lookalike" in res["summary"].lower()
    
    # Impact formatting
    assert len(res["top_features"]) == 2
    assert res["top_features"][0]["impact"] == "+24%"
    assert res["top_features"][1]["impact"] == "+15%"
    
def test_format_explanation_negative_impact():
    top_features = [
        {"name": "uses_https", "importance": -0.12}
    ]
    res = format_explanation("SAFE", top_features, level=3)
    assert res["top_features"][0]["impact"] == "-12%"
