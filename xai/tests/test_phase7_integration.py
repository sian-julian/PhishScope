import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock

@patch("xai.explainer._load_model")
def test_get_shap_values(mock_load):
    mock_model = MagicMock()
    mock_load.return_value = mock_model
    
    with patch("shap.TreeExplainer") as mock_tree:
        mock_explainer = MagicMock()
        mock_tree.return_value = mock_explainer
        # Return list of two arrays to mimic binary classifier
        mock_explainer.shap_values.return_value = [np.array([[0.1, -0.2]]), np.array([[0.3, 0.4]])]
        mock_explainer.expected_value = [0.0, 0.5]
        
        from xai.explainer import get_shap_values
        df = pd.DataFrame([{"feat1": 1, "feat2": 2}])
        shap_vals, base_val = get_shap_values(df)
        
        assert base_val == 0.5
        assert shap_vals.tolist() == [[0.3, 0.4]]

@patch("hybrid.engine.extract_features")
@patch("hybrid.engine.score_url")
@patch("hybrid.engine.predict_url")
@patch("hybrid.engine._prepare_features")
@patch("hybrid.engine.get_shap_values")
def test_analyze_url_with_xai(mock_shap, mock_prepare, mock_predict, mock_score, mock_extract):
    from hybrid.engine import analyze_url
    
    mock_extract.return_value = {"valid": True, "url": "http://test.com"}
    mock_score.return_value = {"score": 90, "verdict": "DANGEROUS"}
    mock_predict.return_value = {"prediction": "PHISHING", "confidence": 0.99}
    
    mock_prepare.return_value = pd.DataFrame([{"lookalike": 1, "entropy": 4.5}])
    mock_shap.return_value = (np.array([[0.24, 0.18]]), 0.5)
    
    result = analyze_url("http://test.com")
    
    assert "explanation" in result
    explanation = result["explanation"]
    assert "summary" in explanation
    assert len(explanation["top_features"]) == 2
    assert explanation["top_features"][0]["feature"] == "lookalike"
    assert explanation["top_features"][0]["impact"] == "+24%"
