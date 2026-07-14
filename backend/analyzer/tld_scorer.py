"""Risk scoring for public suffixes and top-level domains."""

from __future__ import annotations

try:
    from backend.config import TLD_RISK_POINTS, logger
    from backend.utils.loaders import load_suspicious_tlds
except ImportError:  # pragma: no cover - supports `python -m analyzer...` from backend/
    from config import TLD_RISK_POINTS, logger
    from utils.loaders import load_suspicious_tlds

_TLD_GROUPS = load_suspicious_tlds()
HIGH_RISK_TLDS = _TLD_GROUPS.get("high", set())
MEDIUM_RISK_TLDS = _TLD_GROUPS.get("medium", set())


def score_tld(tld: str) -> dict:
    """Score a suffix/TLD using configured phishing-abuse risk groups."""
    tld_lower = tld.lower().strip(".")

    if tld_lower in HIGH_RISK_TLDS:
        risk_level = "high"
    elif tld_lower in MEDIUM_RISK_TLDS:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "tld": tld_lower,
        "risk_level": risk_level,
        "risk_points": TLD_RISK_POINTS[risk_level],
    }


if __name__ == "__main__":
    test_tlds = ["com", "xyz", "tk", "org", "info", "net", "click", "gov"]
    for t in test_tlds:
        logger.info("%s", score_tld(t))
