"""Tests for Phase 6 Hybrid Engine."""

import pytest
from unittest.mock import patch, MagicMock

from hybrid.confidence import calculate_confidence
from hybrid.decision_tree import apply_rules
from hybrid.utils import calculate_hybrid_score, get_hybrid_verdict, build_hybrid_response
from hybrid.engine import analyze_url


def test_calculate_confidence_very_high():
    assert calculate_confidence(0.96) == "VERY_HIGH"

def test_calculate_confidence_high():
    assert calculate_confidence(0.90) == "HIGH"
    
def test_calculate_confidence_medium():
    assert calculate_confidence(0.80) == "MEDIUM"

def test_calculate_confidence_low():
    assert calculate_confidence(0.50) == "LOW"

def test_calculate_confidence_invalid():
    assert calculate_confidence("invalid") == "LOW"


def test_apply_rules_rule1():
    verdict, conf, reasons = apply_rules("DANGEROUS", "PHISHING", "MEDIUM")
    assert verdict == "DANGEROUS"
    assert conf == "VERY_HIGH"
    assert "strongly indicate phishing" in reasons[0]

def test_apply_rules_rule2():
    verdict, conf, reasons = apply_rules("SAFE", "SAFE", "MEDIUM")
    assert verdict == "SAFE"
    assert conf == "HIGH"
    assert "safe" in reasons[0]

def test_apply_rules_rule3():
    verdict, conf, reasons = apply_rules("SAFE", "PHISHING", "MEDIUM")
    assert verdict == "SUSPICIOUS"
    assert conf == "MEDIUM"

def test_apply_rules_rule4():
    verdict, conf, reasons = apply_rules("DANGEROUS", "SAFE", "MEDIUM")
    assert verdict == "SUSPICIOUS"
    assert conf == "MEDIUM"

def test_apply_rules_rule5():
    verdict, conf, reasons = apply_rules("SUSPICIOUS", "PHISHING", "MEDIUM")
    assert verdict == "DANGEROUS"
    assert conf == "HIGH"

def test_apply_rules_no_match():
    verdict, conf, reasons = apply_rules("SUSPICIOUS", "SAFE", "MEDIUM")
    assert verdict is None
    assert conf is None
    assert len(reasons) == 0


def test_calculate_hybrid_score():
    assert calculate_hybrid_score(65, 0.98) == 85  # (65*0.4) + (98*0.6) = 26 + 58.8 = 84.8 -> 85
    assert calculate_hybrid_score(10, 0.10) == 10  # 4 + 6 = 10


def test_get_hybrid_verdict_safe():
    assert get_hybrid_verdict(25) == "SAFE"
    assert get_hybrid_verdict(30) == "SAFE"

def test_get_hybrid_verdict_suspicious():
    assert get_hybrid_verdict(31) == "SUSPICIOUS"
    assert get_hybrid_verdict(60) == "SUSPICIOUS"

def test_get_hybrid_verdict_dangerous():
    assert get_hybrid_verdict(61) == "DANGEROUS"
    assert get_hybrid_verdict(100) == "DANGEROUS"


def test_build_hybrid_response():
    resp = build_hybrid_response({"s": 10}, {"p": "PHISHING"}, 85, "DANGEROUS", "HIGH", ["Test reason"])
    assert "heuristic" in resp
    assert "ml" in resp
    assert resp["hybrid"]["score"] == 85
    assert resp["hybrid"]["verdict"] == "DANGEROUS"
    assert "Test reason" in resp["hybrid"]["reasons"]


@patch("hybrid.engine.extract_features")
@patch("hybrid.engine.score_url")
@patch("hybrid.engine.predict_url")
def test_analyze_url_dangerous_phishing(mock_predict, mock_score, mock_extract):
    mock_extract.return_value = {"valid": True, "url": "http://test.com"}
    mock_score.return_value = {"score": 90, "verdict": "DANGEROUS"}
    mock_predict.return_value = {"prediction": "PHISHING", "confidence": 0.99}
    
    result = analyze_url("http://test.com")
    assert result["hybrid"]["verdict"] == "DANGEROUS"
    assert result["hybrid"]["confidence"] == "VERY_HIGH"
    assert result["hybrid"]["score"] == 95 # (90*0.4)+(99*0.6)=36+59.4=95.4->95

@patch("hybrid.engine.extract_features")
def test_analyze_url_invalid(mock_extract):
    mock_extract.return_value = {"valid": False}
    result = analyze_url("invalid_url")
    assert "error" in result

@patch("hybrid.engine.extract_features")
@patch("hybrid.engine.score_url")
@patch("hybrid.engine.predict_url")
def test_analyze_url_safe_safe(mock_predict, mock_score, mock_extract):
    mock_extract.return_value = {"valid": True, "url": "http://test.com"}
    mock_score.return_value = {"score": 10, "verdict": "SAFE"}
    mock_predict.return_value = {"prediction": "SAFE", "confidence": 0.90}
    
    result = analyze_url("http://test.com")
    assert result["hybrid"]["verdict"] == "SAFE"
    assert result["hybrid"]["confidence"] == "HIGH"
    assert result["hybrid"]["score"] == 10 # (10*0.4)+((1-0.9)*100*0.6)=4+6=10

@patch("hybrid.engine.extract_features")
@patch("hybrid.engine.score_url")
@patch("hybrid.engine.predict_url")
def test_analyze_url_benchmark(mock_predict, mock_score, mock_extract):
    mock_extract.return_value = {"valid": True, "url": "http://test.com"}
    mock_score.return_value = {"score": 50, "verdict": "SUSPICIOUS", "execution_time_ms": 1.2}
    mock_predict.return_value = {"prediction": "SAFE", "confidence": 0.60}
    
    result = analyze_url("http://test.com", benchmark=True)
    assert "execution_time_ms" in result["hybrid"]
    assert "execution_time_ms" not in result["heuristic"]

@patch("hybrid.engine.extract_features")
@patch("hybrid.engine.score_url")
@patch("hybrid.engine.predict_url")
def test_analyze_url_no_rule_match_consensus(mock_predict, mock_score, mock_extract):
    mock_extract.return_value = {"valid": True, "url": "http://test.com"}
    # SUSPICIOUS + SAFE triggers no rule, falls back to consensus calculation
    mock_score.return_value = {"score": 60, "verdict": "SUSPICIOUS"}
    # phishing_prob = 1 - 0.5 = 0.5
    mock_predict.return_value = {"prediction": "SAFE", "confidence": 0.50}
    
    result = analyze_url("http://test.com")
    # Score = (60*0.4) + (50*0.6) = 24 + 30 = 54 -> SUSPICIOUS
    assert result["hybrid"]["verdict"] == "SUSPICIOUS"
    assert result["hybrid"]["confidence"] == "LOW"
    assert "Hybrid engine consensus reached." in result["hybrid"]["reasons"]

@patch("hybrid.engine.extract_features")
@patch("hybrid.engine.score_url")
@patch("hybrid.engine.predict_url")
def test_analyze_url_error_ml(mock_predict, mock_score, mock_extract):
    mock_extract.return_value = {"valid": True, "url": "http://test.com"}
    mock_score.return_value = {"score": 10, "verdict": "SAFE"}
    mock_predict.return_value = {"prediction": "ERROR", "error": "test"}
    
    result = analyze_url("http://test.com")
    # Score = (10*0.4) + (0*0.6) = 4
    assert result["hybrid"]["verdict"] == "SAFE"
