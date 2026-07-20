"""Phase 2 heuristic scoring tests."""

from __future__ import annotations

from copy import deepcopy

import pytest

try:
    from backend.analyzer.feature_extractor import extract_features
    from backend.analyzer.scoring_engine import score_url
except ImportError:  # pragma: no cover - supports running pytest from backend/
    from analyzer.feature_extractor import extract_features
    from analyzer.scoring_engine import score_url


def _clean_features(**overrides: object) -> dict[str, object]:
    """Return a minimal valid feature dictionary with no risk signals."""
    features: dict[str, object] = {
        "valid": True,
        "url": "https://example.com",
        "has_ip_address": False,
        "high_entropy": False,
        "brand_mismatch": False,
        "tld": "com",
        "tld_risk_level": "low",
        "ascii_lookalike_detected": False,
        "unicode_confusable_detected": False,
        "punycode_detected": False,
        "hyphen_count": 0,
        "subdomain_count": 0,
        "has_at_symbol": False,
        "url_length": 19,
        "uses_https": True,
    }
    features.update(overrides)
    return features


@pytest.mark.parametrize("url", ["https://google.com", "https://amazon.com", "https://github.com", "https://microsoft.com"])
def test_safe_urls_are_safe(url: str) -> None:
    result = score_url(extract_features(url))
    assert result["score"] == 0
    assert result["verdict"] == "SAFE"
    assert result["confidence"] == "LOW"


def test_ip_address_rule() -> None:
    result = score_url(_clean_features(has_ip_address=True))
    assert result["score"] == 25
    assert result["reasons"] == ["IP address detected."]


def test_high_entropy_rule() -> None:
    result = score_url(_clean_features(high_entropy=True))
    assert result["score"] == 20
    assert result["reasons"] == ["High entropy detected."]


def test_brand_mismatch_rule() -> None:
    result = score_url(_clean_features(brand_mismatch=True))
    assert result["score"] == 20
    assert result["reasons"] == ["Brand mismatch detected."]


@pytest.mark.parametrize("risk_level", ["high", "medium"])
def test_suspicious_tld_rule(risk_level: str) -> None:
    result = score_url(_clean_features(tld="xyz", tld_risk_level=risk_level))
    assert result["score"] == 15
    assert result["reasons"] == ["Suspicious TLD (.xyz)."]


def test_ip_placeholder_is_not_also_scored_as_tld() -> None:
    result = score_url(
        _clean_features(
            has_ip_address=True,
            tld="N/A (IP address)",
            tld_risk_level="high",
        )
    )
    assert result["score"] == 25
    assert result["triggered_rules"] == 1


@pytest.mark.parametrize(
    ("flag", "expected_reason"),
    [
        ("ascii_lookalike_detected", "ASCII lookalike detected."),
        ("unicode_confusable_detected", "Unicode homograph detected."),
        ("punycode_detected", "Punycode domain detected."),
    ],
)
def test_lookalike_variants_use_one_rule(flag: str, expected_reason: str) -> None:
    result = score_url(_clean_features(**{flag: True}))
    assert result["score"] == 15
    assert result["reasons"] == [expected_reason]


def test_punycode_reason_takes_precedence_over_unicode_reason() -> None:
    result = score_url(_clean_features(punycode_detected=True, unicode_confusable_detected=True))
    assert result["score"] == 15
    assert result["triggered_rules"] == 1
    assert result["reasons"] == ["Punycode domain detected."]


def test_hyphen_threshold_is_inclusive() -> None:
    result = score_url(_clean_features(hyphen_count=3))
    assert result["score"] == 10
    assert result["reasons"] == ["URL contains 3+ hyphens."]


def test_subdomain_threshold_is_inclusive() -> None:
    result = score_url(_clean_features(subdomain_count=4))
    assert result["score"] == 10
    assert result["reasons"] == ["URL contains 4+ subdomains."]


def test_at_symbol_rule() -> None:
    result = score_url(_clean_features(has_at_symbol=True))
    assert result["score"] == 10
    assert result["reasons"] == ["URL contains an @ symbol."]


@pytest.mark.parametrize("url_length", [75, 76])
def test_long_url_rule_is_strictly_greater_than_threshold(url_length: int) -> None:
    result = score_url(_clean_features(url_length=url_length))
    assert result["score"] == (0 if url_length == 75 else 5)


@pytest.mark.parametrize(
    ("score_features", "verdict", "confidence"),
    [
        ({"brand_mismatch": True}, "SAFE", "LOW"),
        ({"brand_mismatch": True, "tld": "xyz", "tld_risk_level": "high"}, "SUSPICIOUS", "MEDIUM"),
        ({"has_ip_address": True, "high_entropy": True, "brand_mismatch": True}, "DANGEROUS", "HIGH"),
    ],
)
def test_verdict_and_confidence_bands(
    score_features: dict[str, object], verdict: str, confidence: str
) -> None:
    result = score_url(_clean_features(**score_features))
    assert result["verdict"] == verdict
    assert result["confidence"] == confidence


def test_score_is_capped_at_100() -> None:
    result = score_url(
        _clean_features(
            has_ip_address=True,
            high_entropy=True,
            brand_mismatch=True,
            tld="xyz",
            tld_risk_level="high",
            ascii_lookalike_detected=True,
            hyphen_count=3,
            subdomain_count=4,
            has_at_symbol=True,
            url_length=76,
        )
    )
    assert result["score"] == 100
    assert result["triggered_rules"] == 9


def test_reasons_and_trigger_count_cover_each_rule() -> None:
    result = score_url(
        _clean_features(
            high_entropy=True,
            brand_mismatch=True,
            tld="tk",
            tld_risk_level="high",
            ascii_lookalike_detected=True,
            hyphen_count=3,
        )
    )
    assert result["score"] == 80
    assert result["triggered_rules"] == len(result["reasons"]) == 5


def test_scoring_keeps_original_feature_dictionary() -> None:
    features = _clean_features(brand_mismatch=True)
    result = score_url(features)
    assert result["features"] is features
    assert features == _clean_features(brand_mismatch=True)


def test_invalid_feature_result_is_returned_without_risk_score() -> None:
    features = {"valid": False, "reason": "Invalid URL", "url": "abc"}
    result = score_url(features)
    assert result["score"] == 0
    assert result["triggered_rules"] == 0
    assert result["reasons"] == ["Invalid URL."]
    assert result["features"] == features


def test_non_dictionary_features_are_rejected() -> None:
    with pytest.raises(TypeError, match="features must be a dictionary"):
        score_url([])  # type: ignore[arg-type]


def test_benchmarking_is_optional() -> None:
    features = extract_features("https://google.com")
    assert "execution_time_ms" not in score_url(features)
    assert score_url(features, benchmark=True)["execution_time_ms"] >= 0


def test_integration_g00gle_xyz_exposes_requested_risk_signals() -> None:
    result = score_url(extract_features("https://g00gle.xyz"))
    assert result["score"] == 30
    assert result["verdict"] == "SAFE"
    assert result["reasons"] == ["Suspicious TLD (.xyz).", "ASCII lookalike detected."]


def test_integration_secure_hdfc_login_verify_is_dangerous() -> None:
    result = score_url(extract_features("https://secure-hdfc-login-verify.xyz"))
    assert result["score"] == 65
    assert result["verdict"] == "DANGEROUS"
    assert result["triggered_rules"] == 4


def test_integration_medium_risk_brand_domain_is_suspicious() -> None:
    result = score_url(extract_features("paypal-check.info"))
    assert result["score"] == 35
    assert result["verdict"] == "SUSPICIOUS"


def test_input_features_are_not_mutated() -> None:
    features = _clean_features(high_entropy=True)
    original = deepcopy(features)
    score_url(features, benchmark=True)
    assert features == original
