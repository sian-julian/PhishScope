"""Core lexical feature extraction for PhishScope URL analysis."""

from __future__ import annotations

import re
from time import perf_counter
from urllib.parse import urlparse

try:
    from .brand_checker import check_brand_position, extract_domain_parts
    from .entropy import is_high_entropy, shannon_entropy
    from .lookalike import check_lookalike
    from .tld_scorer import score_tld
except ImportError:  # pragma: no cover - supports direct import from backend/
    from analyzer.brand_checker import check_brand_position, extract_domain_parts
    from analyzer.entropy import is_high_entropy, shannon_entropy
    from analyzer.lookalike import check_lookalike
    from analyzer.tld_scorer import score_tld

try:
    from backend.config import (
        HIGH_URL_LENGTH_THRESHOLD,
        IP_RISK_POINTS,
        MEDIUM_URL_LENGTH_THRESHOLD,
        URL_LENGTH_RISK_POINTS,
        logger,
    )
    from backend.utils.loaders import load_brands
    from backend.utils.validators import validate_url
except ImportError:  # pragma: no cover - supports `python -m analyzer...` from backend/
    from config import (
        HIGH_URL_LENGTH_THRESHOLD,
        IP_RISK_POINTS,
        MEDIUM_URL_LENGTH_THRESHOLD,
        URL_LENGTH_RISK_POINTS,
        logger,
    )
    from utils.loaders import load_brands
    from utils.validators import validate_url

DEFAULT_BRANDS = load_brands()


def _digit_ratio(text: str) -> float:
    """Return the ratio of digit characters to total characters."""
    if not text:
        return 0.0
    digits = sum(ch.isdigit() for ch in text)
    return round(digits / len(text), 4)


def _score_url_length(url_length: int) -> dict[str, int | str]:
    """Score URL length using configured thresholds."""
    if url_length >= HIGH_URL_LENGTH_THRESHOLD:
        risk_level = "high"
    elif url_length >= MEDIUM_URL_LENGTH_THRESHOLD:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "risk_level": risk_level,
        "risk_points": URL_LENGTH_RISK_POINTS[risk_level],
    }


def _elapsed_ms(start_time: float) -> float:
    """Return elapsed milliseconds from a perf_counter start point."""
    return round((perf_counter() - start_time) * 1000, 4)


def extract_features(url: str, brand_list: list[str] | None = None, benchmark: bool = False) -> dict:
    """Extract lexical and structural phishing features from one URL."""
    analysis_start = perf_counter()
    brands = brand_list if brand_list is not None else DEFAULT_BRANDS

    validation = validate_url(url)
    if not validation.valid:
        logger.warning("Invalid URL rejected: %s", validation.normalized_url)
        result: dict[str, object] = {
            "valid": False,
            "reason": validation.reason,
            "url": validation.normalized_url,
        }
        if benchmark:
            result["benchmark"] = {"url_analysis_ms": _elapsed_ms(analysis_start)}
        return result

    raw_url = validation.normalized_url
    working_url = validation.working_url
    parsed = urlparse(working_url)
    host = validation.host

    is_ip = validation.is_ip_address
    domain_parts = extract_domain_parts(working_url)

    lookalike_start = perf_counter()
    lookalike_result = check_lookalike(host, brands)
    lookalike_ms = _elapsed_ms(lookalike_start)

    brand_start = perf_counter()
    brand_result = check_brand_position(working_url, brands)
    brand_ms = _elapsed_ms(brand_start)

    if is_ip:
        tld_result = {"tld": "N/A (IP address)", "risk_level": "high", "risk_points": IP_RISK_POINTS}
        domain_for_entropy = host
    else:
        tld_result = score_tld(domain_parts["tld"])
        domain_for_entropy = domain_parts["registered_domain"] or host

    entropy_start = perf_counter()
    entropy = shannon_entropy(domain_for_entropy)
    entropy_ms = _elapsed_ms(entropy_start)
    url_length_result = _score_url_length(len(raw_url))

    features: dict[str, object] = {
        "valid": True,
        "reason": None,
        "url": raw_url,
        "host": host,
        "url_length": len(raw_url),
        "url_length_risk_level": url_length_result["risk_level"],
        "url_length_risk_points": url_length_result["risk_points"],
        "dot_count": host.count("."),
        "hyphen_count": host.count("-"),
        "has_ip_address": is_ip,
        "has_at_symbol": "@" in raw_url,
        "subdomain_count": len(domain_parts["subdomain"].split(".")) if domain_parts["subdomain"] else 0,
        "uses_https": parsed.scheme == "https",
        "digit_ratio": _digit_ratio(host),
        "token_count": len(re.split(r"[.\-]", host)),

        "shannon_entropy": entropy,
        "high_entropy": is_high_entropy(domain_for_entropy),

        "tld": tld_result["tld"],
        "tld_risk_level": tld_result["risk_level"],
        "tld_risk_points": tld_result["risk_points"],

        "brand_found": brand_result["brand_found"],
        "brand_position": brand_result["position"],
        "brand_mismatch": brand_result["is_suspicious"],
        "brand_risk_points": brand_result["risk_points"],

        "ascii_lookalike_detected": lookalike_result["ascii_lookalike_detected"],
        "unicode_confusable_detected": lookalike_result["unicode_confusable_detected"],
        "punycode_detected": lookalike_result["punycode_detected"],
        "decoded_domain": lookalike_result["decoded_domain"],
        "normalized_decoded_domain": lookalike_result["normalized_decoded_domain"],
        "lookalike_matched_brand": lookalike_result["matched_brand"],
        "lookalike_risk_points": lookalike_result["risk_points"],
    }

    if benchmark:
        features["benchmark"] = {
            "url_analysis_ms": _elapsed_ms(analysis_start),
            "entropy_calculation_ms": entropy_ms,
            "lookalike_detection_ms": lookalike_ms,
            "brand_detection_ms": brand_ms,
        }

    return features


if __name__ == "__main__":
    test_urls = [
        "https://hdfc.com/login",
        "http://192.168.1.10/login/verify",
        "https://secure-hdfc-login-verify.xyz/account/confirm",
        "https://g00gle.com/accounts",
        "https://xn--pypal-4ve.com/signin",
        "https://www.amazon.com/gp/orders",
        "https://xk92mz-portal.tk/reset-password",
    ]

    for u in test_urls:
        logger.info("%s", "=" * 100)
        logger.info("URL: %s", u)
        f = extract_features(u, benchmark=True)
        for k, v in f.items():
            logger.info("  %-30s: %s", k, v)
