"""Automated tests for Phase 5 Machine Learning."""

import json
from pathlib import Path

import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier
import joblib

from ml.scripts.common import (
    EVALUATION_DIR,
    MODELS_DIR,
    TRAIN_PATH,
    TEST_PATH,
)
from ml.scripts.train import train_model, load_training_data
from ml.scripts.evaluate import evaluate_model
from ml.scripts.predict import predict_url, predict_batch, _MODEL_CACHE, _prepare_features


@pytest.fixture(autouse=True)
def mock_directories(monkeypatch, tmp_path):
    """Override standard paths to use temporary directories for testing."""
    test_models = tmp_path / "models"
    test_eval = tmp_path / "evaluation"
    test_models.mkdir()
    test_eval.mkdir()
    
    monkeypatch.setattr("ml.scripts.common.MODELS_DIR", test_models)
    monkeypatch.setattr("ml.scripts.train.MODELS_DIR", test_models)
    monkeypatch.setattr("ml.scripts.evaluate.MODELS_DIR", test_models)
    monkeypatch.setattr("ml.scripts.predict.MODELS_DIR", test_models)
    
    monkeypatch.setattr("ml.scripts.common.EVALUATION_DIR", test_eval)
    monkeypatch.setattr("ml.scripts.train.EVALUATION_DIR", test_eval)
    monkeypatch.setattr("ml.scripts.evaluate.EVALUATION_DIR", test_eval)
    
    monkeypatch.setattr("ml.scripts.predict._MODEL_CACHE", None)
    
    return tmp_path


@pytest.fixture
def mock_dataset(tmp_path, monkeypatch):
    """Create a small mock dataset."""
    train_file = tmp_path / "train.csv"
    test_file = tmp_path / "test.csv"
    
    # 5 safe, 5 phishing for train
    data = {
        "url": [f"http://example{i}.com" for i in range(10)],
        "source": ["mock"] * 10,
        "tld_risk_level": ["low"] * 10,
        "brand_position": [""] * 10,
        "lookalike_matched_brand": [""] * 10,
        "label": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
        "entropy": [1.0, 1.2, 1.1, 1.0, 1.3, 3.5, 4.0, 3.8, 4.1, 3.9],
        "tld_score": [0, 0, 0, 0, 0, 10, 15, 10, 20, 10]
    }
    df = pd.DataFrame(data)
    df.to_csv(train_file, index=False)
    df.to_csv(test_file, index=False)
    
    monkeypatch.setattr("ml.scripts.train.TRAIN_PATH", train_file)
    monkeypatch.setattr("ml.scripts.evaluate.TEST_PATH", test_file)
    
    return train_file, test_file


def test_load_training_data_success(mock_dataset):
    X, y = load_training_data(mock_dataset[0])
    assert len(X) == 10
    assert len(y) == 10
    assert "url" not in X.columns
    assert "label" not in X.columns
    assert "entropy" in X.columns


def test_load_training_data_missing():
    with pytest.raises(FileNotFoundError):
        load_training_data(Path("nonexistent.csv"))


def test_load_training_data_empty(tmp_path):
    empty_csv = tmp_path / "empty.csv"
    pd.DataFrame().to_csv(empty_csv, index=False)
    with pytest.raises(ValueError):
        load_training_data(empty_csv)


def test_train_model_saves_pkl(mock_dataset, mock_directories):
    train_model(benchmark=False)
    assert (mock_directories / "models" / "random_forest.pkl").exists()


def test_train_model_saves_metadata(mock_dataset, mock_directories):
    train_model(benchmark=False)
    meta_path = mock_directories / "models" / "model_metadata.json"
    assert meta_path.exists()
    
    with open(meta_path, "r") as f:
        meta = json.load(f)
        assert meta["model"] == "Random Forest"
        assert meta["training_rows"] == 10


def test_train_model_benchmark_saves_best_model(mock_dataset, mock_directories):
    train_model(benchmark=True)
    assert (mock_directories / "models" / "best_model.pkl").exists()
    assert (mock_directories / "evaluation" / "model_comparison.csv").exists()


def test_train_model_returns_stats(mock_dataset):
    stats = train_model(benchmark=True)
    assert "model_name" in stats
    assert "training_rows" in stats
    assert "execution_time_ms" in stats


def test_evaluate_missing_model(mock_dataset):
    with pytest.raises(FileNotFoundError):
        evaluate_model()


def test_evaluate_metrics_json_generated(mock_dataset, mock_directories):
    train_model(benchmark=False)
    evaluate_model()
    metrics_path = mock_directories / "evaluation" / "metrics.json"
    assert metrics_path.exists()
    with open(metrics_path, "r") as f:
        metrics = json.load(f)
        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1_score" in metrics


def test_evaluate_classification_report(mock_dataset, mock_directories):
    train_model(benchmark=False)
    evaluate_model()
    assert (mock_directories / "evaluation" / "classification_report.txt").exists()


def test_evaluate_confusion_matrix(mock_dataset, mock_directories):
    train_model(benchmark=False)
    evaluate_model()
    assert (mock_directories / "evaluation" / "confusion_matrix.png").exists()


def test_evaluate_roc_curve(mock_dataset, mock_directories):
    train_model(benchmark=False)
    evaluate_model()
    assert (mock_directories / "evaluation" / "roc_curve.png").exists()


def test_evaluate_feature_importance(mock_dataset, mock_directories):
    train_model(benchmark=False)
    evaluate_model()
    assert (mock_directories / "evaluation" / "feature_importance.csv").exists()


def test_evaluate_returns_stats(mock_dataset, mock_directories):
    train_model(benchmark=False)
    stats = evaluate_model(benchmark=True)
    assert "test_rows" in stats
    assert "accuracy" in stats
    assert "execution_time_ms" in stats


def test_prepare_features_invalid_url():
    with pytest.raises(ValueError, match="Invalid URL"):
        _prepare_features("not_a_url")


def test_predict_url_success(mock_dataset, monkeypatch):
    train_model(benchmark=False)
    
    def mock_extract(url, *args, **kwargs):
        return {
            "valid": True, "shannon_entropy": 4.5, "tld_risk_points": 20, 
            "tld_risk_level": "high", "brand_mismatch": True, "brand_position": "",
            "ascii_lookalike_detected": False, "unicode_confusable_detected": False,
            "punycode_detected": False, "has_ip_address": False, "url_length": 80,
            "subdomain_count": 3, "hyphen_count": 2, "has_at_symbol": False,
            "digit_ratio": 0.1, "token_count": 5, "dot_count": 3, "uses_https": True,
            "high_entropy": True, "url_length_risk_points": 5, "lookalike_matched_brand": ""
        }
    
    monkeypatch.setattr("ml.scripts.predict.extract_features", mock_extract)
    
    # Needs a mock prepare features so it doesn't fail on missing columns trained on
    def mock_prepare(*args, **kwargs):
        return pd.DataFrame([{"entropy": 4.5, "tld_score": 20}])
    monkeypatch.setattr("ml.scripts.predict._prepare_features", mock_prepare)
    
    result = predict_url("http://example.com")
    assert "prediction" in result
    assert "confidence" in result


def test_predict_url_error_handling():
    result = predict_url("invalid_url")
    assert result["prediction"] == "ERROR"
    assert "error" in result


def test_predict_batch(mock_dataset, monkeypatch):
    train_model(benchmark=False)
    def mock_prepare(*args, **kwargs):
        return pd.DataFrame([{"entropy": 4.5, "tld_score": 20}])
    monkeypatch.setattr("ml.scripts.predict._prepare_features", mock_prepare)
    
    results = predict_batch(["http://example.com", "http://example2.com"])
    assert len(results) == 2
    assert results[0]["prediction"] in ["SAFE", "PHISHING"]
    assert results[1]["prediction"] in ["SAFE", "PHISHING"]


def test_evaluate_with_best_model_fallback(mock_dataset, mock_directories):
    train_model(benchmark=True) # saves best_model.pkl
    assert not (mock_directories / "models" / "random_forest.pkl").exists()
    evaluate_model() # Should not raise error
    assert (mock_directories / "evaluation" / "metrics.json").exists()


def test_model_caching(mock_dataset, mock_directories, monkeypatch):
    train_model(benchmark=False)
    
    def mock_prepare(*args, **kwargs):
        return pd.DataFrame([{"entropy": 4.5, "tld_score": 20}])
    monkeypatch.setattr("ml.scripts.predict._prepare_features", mock_prepare)
    
    predict_url("http://example.com")
    
    import ml.scripts.predict
    assert ml.scripts.predict._MODEL_CACHE is not None
    
    # Delete model to prove it uses cache
    (mock_directories / "models" / "random_forest.pkl").unlink()
    
    result = predict_url("http://example.com")
    assert result["prediction"] != "ERROR"


def test_evaluate_roc_fallback(mock_dataset, mock_directories, monkeypatch):
    """Test ROC fallback if predict_proba is missing."""
    train_model(benchmark=False)
    
    # Mock the loaded model to not have predict_proba
    original_load = joblib.load
    
    class NoProbaWrapper:
        def __init__(self, model):
            self.model = model
        def predict(self, X):
            return self.model.predict(X)
            
    def mock_load(*args, **kwargs):
        m = original_load(*args, **kwargs)
        return NoProbaWrapper(m)
        
    monkeypatch.setattr("joblib.load", mock_load)
    
    evaluate_model()
    # Should still succeed without error
    metrics_path = mock_directories / "evaluation" / "metrics.json"
    assert metrics_path.exists()
