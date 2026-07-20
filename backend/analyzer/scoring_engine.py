"""Explainable heuristic scoring for PhishScope URL features."""

from __future__ import annotations

from collections.abc import Callable
from time import perf_counter
from typing import Any

try:
    from backend.config import (
        AT_SYMBOL_POINTS,
        BRAND_POINTS,
        ENABLE_MISSING_HTTPS_RULE,
        ENTROPY_POINTS,
        HYPHEN_POINTS,
        HYPHEN_THRESHOLD,
        IP_RISK_POINTS,
        LONG_URL_POINTS,
        LONG_URL_THRESHOLD,
        LOOKALIKE_POINTS,
        MAX_RISK_SCORE,
        MISSING_HTTPS_POINTS,
        SAFE_SCORE_MAX,
        SUBDOMAIN_POINTS,
        SUBDOMAIN_THRESHOLD,
        SUSPICIOUS_SCORE_MAX,
        SUSPICIOUS_TLD_POINTS,
        SUSPICIOUS_TLD_RISK_LEVELS,
        logger,
    )
except ImportError:  # pragma: no cover - supports `python -m analyzer...` from backend/
    from config import (
        AT_SYMBOL_POINTS,
        BRAND_POINTS,
        ENABLE_MISSING_HTTPS_RULE,
        ENTROPY_POINTS,
        HYPHEN_POINTS,
        HYPHEN_THRESHOLD,
        IP_RISK_POINTS,
        LONG_URL_POINTS,
        LONG_URL_THRESHOLD,
        LOOKALIKE_POINTS,
        MAX_RISK_SCORE,
        MISSING_HTTPS_POINTS,
        SAFE_SCORE_MAX,
        SUBDOMAIN_POINTS,
        SUBDOMAIN_THRESHOLD,
        SUSPICIOUS_SCORE_MAX,
        SUSPICIOUS_TLD_POINTS,
        SUSPICIOUS_TLD_RISK_LEVELS,
        logger,
    )

Rule = tuple[Callable[[dict[str, Any]], bool], int, Callable[[dict[str, Any]], str]]


def _has_lookalike(features: dict[str, Any]) -> bool:
    """Return whether any Phase 1 lookalike signal is present."""
    return any(
        bool(features.get(key))
        for key in (
            "ascii_lookalike_detected",
            "unicode_confusable_detected",
            "punycode_detected",
        )
    )


def _lookalike_reason(features: dict[str, Any]) -> str:
    """Return the most specific available lookalike explanation."""
    if features.get("punycode_detected"):
        return "Punycode domain detected."
    if features.get("unicode_confusable_detected"):
        return "Unicode homograph detected."
    return "ASCII lookalike detected."


def _has_suspicious_tld(features: dict[str, Any]) -> bool:
    """Return whether a non-IP URL uses a configured risky TLD class."""
    return (
        features.get("tld") != "N/A (IP address)"
        and features.get("tld_risk_level") in SUSPICIOUS_TLD_RISK_LEVELS
    )


RULES: tuple[Rule, ...] = (
    (
        lambda features: bool(features.get("has_ip_address")),
        IP_RISK_POINTS,
        lambda features: "IP address detected.",
    ),
    (
        lambda features: bool(features.get("high_entropy")),
        ENTROPY_POINTS,
        lambda features: "High entropy detected.",
    ),
    (
        lambda features: bool(features.get("brand_mismatch")),
        BRAND_POINTS,
        lambda features: "Brand mismatch detected.",
    ),
    (
        _has_suspicious_tld,
        SUSPICIOUS_TLD_POINTS,
        lambda features: f"Suspicious TLD (.{features.get('tld')}).",
    ),
    (_has_lookalike, LOOKALIKE_POINTS, _lookalike_reason),
    (
        lambda features: int(features.get("hyphen_count", 0)) >= HYPHEN_THRESHOLD,
        HYPHEN_POINTS,
        lambda features: f"URL contains {HYPHEN_THRESHOLD}+ hyphens.",
    ),
    (
        lambda features: int(features.get("subdomain_count", 0)) >= SUBDOMAIN_THRESHOLD,
        SUBDOMAIN_POINTS,
        lambda features: f"URL contains {SUBDOMAIN_THRESHOLD}+ subdomains.",
    ),
    (
        lambda features: bool(features.get("has_at_symbol")),
        AT_SYMBOL_POINTS,
        lambda features: "URL contains an @ symbol.",
    ),
    (
        lambda features: int(features.get("url_length", 0)) > LONG_URL_THRESHOLD,
        LONG_URL_POINTS,
        lambda features: f"URL exceeds {LONG_URL_THRESHOLD} characters.",
    ),
)


def _verdict_and_confidence(score: int) -> tuple[str, str]:
    """Map a bounded score to its verdict and confidence level."""
    if score <= SAFE_SCORE_MAX:
        return "SAFE", "LOW"
    if score <= SUSPICIOUS_SCORE_MAX:
        return "SUSPICIOUS", "MEDIUM"
    return "DANGEROUS", "HIGH"


def score_url(features: dict[str, Any], benchmark: bool = False) -> dict[str, Any]:
    """Score Phase 1 features and return an explainable phishing verdict.

    Invalid feature results are retained in the response but do not receive a
    phishing score because no URL analysis was completed.
    """
    if not isinstance(features, dict):
        raise TypeError("features must be a dictionary returned by extract_features")

    start_time = perf_counter()
    if features.get("valid") is False:
        response: dict[str, Any] = {
            "score": 0,
            "verdict": "SAFE",
            "confidence": "LOW",
            "triggered_rules": 0,
            "reasons": ["Invalid URL."],
            "features": features,
        }
        if benchmark:
            response["execution_time_ms"] = round((perf_counter() - start_time) * 1000, 4)
        logger.warning("Invalid feature set received by scoring engine")
        return response

    score = 0
    reasons: list[str] = []

    for predicate, points, reason_builder in RULES:
        if predicate(features):
            score += points
            reasons.append(reason_builder(features))

    if ENABLE_MISSING_HTTPS_RULE and not features.get("uses_https"):
        score += MISSING_HTTPS_POINTS
        reasons.append("URL does not use HTTPS.")

    score = min(score, MAX_RISK_SCORE)
    verdict, confidence = _verdict_and_confidence(score)
    response = {
        "score": score,
        "verdict": verdict,
        "confidence": confidence,
        "triggered_rules": len(reasons),
        "reasons": reasons,
        "features": features,
    }

    if benchmark:
        response["execution_time_ms"] = round((perf_counter() - start_time) * 1000, 4)

    logger.info("URL scored as %s (%d)", verdict, score)
    if verdict != "SAFE":
        logger.warning("Suspicious URL indicators: %s", "; ".join(reasons))

    return response


if __name__ == "__main__":
    try:
        from .feature_extractor import extract_features
    except ImportError:  # pragma: no cover - supports `python -m analyzer...` from backend/
        from analyzer.feature_extractor import extract_features

    for sample_url in ("https://google.com", "https://secure-hdfc-login-verify.xyz"):
        logger.info("%s", score_url(extract_features(sample_url), benchmark=True))
