"""Phase 1 feature extraction tests."""

from __future__ import annotations

import pytest

try:
    from backend.analyzer.brand_checker import extract_domain_parts
    from backend.analyzer.feature_extractor import extract_features
    from backend.analyzer.lookalike import check_lookalike, decode_punycode_domain
    from backend.utils.validators import is_valid_ip, normalize_url, validate_url
except ImportError:  # pragma: no cover - supports running pytest from backend/
    from analyzer.brand_checker import extract_domain_parts
    from analyzer.feature_extractor import extract_features
    from analyzer.lookalike import check_lookalike, decode_punycode_domain
    from utils.validators import is_valid_ip, normalize_url, validate_url


def test_legacy_legit_hdfc_has_low_risk_indicators() -> None:
    features = extract_features("https://hdfc.com/login")
    assert features["valid"] is True
    assert features["brand_mismatch"] is False
    assert features["tld_risk_points"] == 0
    assert features["lookalike_risk_points"] == 0


def test_legacy_ip_url_is_flagged() -> None:
    features = extract_features("http://192.168.1.10/login/verify")
    assert features["has_ip_address"] is True
    assert features["tld_risk_points"] == 25


def test_legacy_fake_hdfc_domain_is_flagged() -> None:
    features = extract_features("https://secure-hdfc-login-verify.xyz/account/confirm")
    assert features["brand_mismatch"] is True
    assert features["tld_risk_level"] == "high"
    assert features["shannon_entropy"] > 3.5


def test_legacy_ascii_lookalike_is_flagged() -> None:
    features = extract_features("https://g00gle.com/accounts")
    assert features["ascii_lookalike_detected"] is True
    assert features["lookalike_matched_brand"] == "google"


def test_legacy_punycode_is_detected() -> None:
    features = extract_features("https://xn--pypal-4ve.com/signin")
    assert features["punycode_detected"] is True


def test_legacy_www_amazon_is_not_brand_mismatch() -> None:
    features = extract_features("https://www.amazon.com/gp/orders")
    assert features["brand_mismatch"] is False


@pytest.mark.parametrize(
    ("url", "subdomain", "domain", "suffix"),
    [
        ("paypal.co.uk", "", "paypal", "co.uk"),
        ("amazon.co.in", "", "amazon", "co.in"),
        ("mail.google.com", "mail", "google", "com"),
        ("secure.login.microsoft.co.uk", "secure.login", "microsoft", "co.uk"),
        ("bbc.co.uk", "", "bbc", "co.uk"),
    ],
)
def test_public_suffix_domain_parsing(url: str, subdomain: str, domain: str, suffix: str) -> None:
    parts = extract_domain_parts(url)
    assert parts["subdomain"] == subdomain
    assert parts["registered_domain"] == domain
    assert parts["tld"] == suffix


def test_public_suffix_legitimate_paypal_is_not_mismatch() -> None:
    features = extract_features("https://paypal.co.uk/login")
    assert features["brand_found"] == "paypal"
    assert features["brand_position"] == "registered_domain"
    assert features["brand_mismatch"] is False


def test_public_suffix_legitimate_amazon_india_is_not_mismatch() -> None:
    features = extract_features("https://amazon.co.in/orders")
    assert features["brand_found"] == "amazon"
    assert features["brand_position"] == "registered_domain"
    assert features["brand_mismatch"] is False


def test_public_suffix_nested_microsoft_is_not_mismatch() -> None:
    features = extract_features("https://secure.login.microsoft.co.uk")
    assert features["brand_found"] == "microsoft"
    assert features["brand_mismatch"] is False
    assert features["subdomain_count"] == 2


def test_brand_in_subdomain_on_public_suffix_is_mismatch() -> None:
    features = extract_features("https://paypal.secure-login.co.uk")
    assert features["brand_position"] == "subdomain"
    assert features["brand_mismatch"] is True


def test_embedded_brand_on_public_suffix_is_mismatch() -> None:
    features = extract_features("https://secure-paypal-login.co.uk")
    assert features["brand_position"] == "embedded"
    assert features["brand_mismatch"] is True


def test_userinfo_host_extraction() -> None:
    features = extract_features("admin:123@google.com")
    assert features["valid"] is True
    assert features["host"] == "google.com"
    assert features["has_at_symbol"] is True
    assert features["brand_mismatch"] is False


def test_userinfo_with_https_host_extraction() -> None:
    features = extract_features("https://admin:password@google.com/login")
    assert features["valid"] is True
    assert features["host"] == "google.com"
    assert features["has_at_symbol"] is True


def test_port_is_removed_from_host() -> None:
    features = extract_features("https://google.com:8080")
    assert features["valid"] is True
    assert features["host"] == "google.com"
    assert features["brand_found"] == "google"


def test_ipv4_validity_helper_accepts_valid_ip() -> None:
    assert is_valid_ip("127.0.0.1") is True
    assert is_valid_ip("192.168.1.10") is True


def test_ipv6_validity_helper_accepts_valid_ip() -> None:
    assert is_valid_ip("2001:db8::1") is True


def test_ip_validity_helper_rejects_invalid_ip() -> None:
    assert is_valid_ip("999.999.999.999") is False


def test_ipv6_url_is_flagged_as_ip_address() -> None:
    features = extract_features("https://[2001:db8::1]")
    assert features["valid"] is True
    assert features["host"] == "2001:db8::1"
    assert features["has_ip_address"] is True
    assert features["tld_risk_points"] == 25


def test_invalid_ipv4_like_host_is_invalid_url() -> None:
    features = extract_features("https://999.999.999.999")
    assert features["valid"] is False
    assert features["reason"] == "Invalid URL"


def test_uppercase_url_is_normalized() -> None:
    features = extract_features("HTTPS://GOOGLE.COM")
    assert features["valid"] is True
    assert features["url"] == "https://google.com"
    assert features["host"] == "google.com"


def test_whitespace_tabs_and_newlines_are_normalized() -> None:
    assert normalize_url(" GOOGLE.COM\n\t") == "google.com"


@pytest.mark.parametrize("url", ["abc", "....", "////", "http://", "", "   "])
def test_invalid_urls_return_invalid_result(url: str) -> None:
    features = extract_features(url)
    assert features["valid"] is False
    assert features["reason"] == "Invalid URL"


def test_validator_accepts_bare_domain() -> None:
    result = validate_url("google.com")
    assert result.valid is True
    assert result.host == "google.com"


def test_validator_accepts_localhost() -> None:
    result = validate_url("localhost")
    assert result.valid is True
    assert result.host == "localhost"


def test_localhost_feature_extraction_is_valid() -> None:
    features = extract_features("localhost")
    assert features["valid"] is True
    assert features["host"] == "localhost"
    assert features["tld"] == ""


def test_loopback_feature_extraction_is_valid_ip() -> None:
    features = extract_features("127.0.0.1")
    assert features["valid"] is True
    assert features["has_ip_address"] is True


def test_unicode_confusable_paypal_is_detected() -> None:
    features = extract_features("https://раypal.com")
    assert features["unicode_confusable_detected"] is True
    assert features["lookalike_matched_brand"] == "paypal"


def test_punycode_domain_decodes_to_unicode() -> None:
    decoded = decode_punycode_domain("xn--pypal-4ve.com")
    assert decoded.endswith(".com")
    assert decoded != "xn--pypal-4ve.com"


def test_punycode_domain_matches_brand_after_normalization() -> None:
    features = extract_features("https://xn--pypal-4ve.com/signin")
    assert features["punycode_detected"] is True
    assert features["unicode_confusable_detected"] is True
    assert features["normalized_decoded_domain"] == "paypal.com"
    assert features["lookalike_matched_brand"] == "paypal"


def test_check_lookalike_punycode_result_includes_decoded_domain() -> None:
    result = check_lookalike("xn--pypal-4ve.com", ["paypal"])
    assert result["punycode_detected"] is True
    assert result["decoded_domain"] is not None
    assert result["normalized_decoded_domain"] == "paypal.com"


def test_long_high_risk_url_sets_expected_signals() -> None:
    features = extract_features("https://secure-login-verification-hdfc-account-update.xyz/login")
    assert features["valid"] is True
    assert features["brand_mismatch"] is True
    assert features["tld_risk_level"] == "high"
    assert features["url_length"] > 50


def test_url_length_risk_fields_are_available() -> None:
    features = extract_features("https://secure-login-verification-hdfc-account-update.xyz/login")
    assert "url_length_risk_level" in features
    assert "url_length_risk_points" in features


def test_high_entropy_flag_is_available() -> None:
    features = extract_features("https://xk92mz-portal.tk/reset-password")
    assert "high_entropy" in features
    assert features["tld_risk_level"] == "high"


def test_benchmark_output_is_optional() -> None:
    features = extract_features("https://google.com", benchmark=True)
    assert "benchmark" in features
    assert "url_analysis_ms" in features["benchmark"]
    assert "entropy_calculation_ms" in features["benchmark"]
    assert "lookalike_detection_ms" in features["benchmark"]
    assert "brand_detection_ms" in features["benchmark"]


def test_benchmark_output_is_not_returned_by_default() -> None:
    features = extract_features("https://google.com")
    assert "benchmark" not in features


def test_mail_google_subdomain_count() -> None:
    features = extract_features("https://mail.google.com")
    assert features["valid"] is True
    assert features["subdomain_count"] == 1
    assert features["brand_mismatch"] is False


def test_google_co_uk_suffix_is_preserved() -> None:
    features = extract_features("https://google.co.uk")
    assert features["valid"] is True
    assert features["tld"] == "co.uk"
    assert features["brand_found"] == "google"


def test_https_flag_for_https_url() -> None:
    features = extract_features("https://google.com")
    assert features["uses_https"] is True


def test_https_flag_for_bare_url_defaults_to_http() -> None:
    features = extract_features("google.com")
    assert features["uses_https"] is False


def test_invalid_url_with_benchmark_still_returns_timing() -> None:
    features = extract_features("abc", benchmark=True)
    assert features["valid"] is False
    assert "benchmark" in features
