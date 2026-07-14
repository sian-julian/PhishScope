"""Entropy helpers for detecting random-looking domain strings."""

from __future__ import annotations

import math
from collections import Counter

try:
    from backend.config import HIGH_ENTROPY_THRESHOLD, logger
except ImportError:  # pragma: no cover - supports `python -m analyzer...` from backend/
    from config import HIGH_ENTROPY_THRESHOLD, logger


def shannon_entropy(text: str) -> float:
    """Compute Shannon entropy for a domain-like string."""
    if not text:
        return 0.0

    length = len(text)
    frequency = Counter(text)

    entropy = 0.0
    for count in frequency.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return round(entropy, 4)


def is_high_entropy(text: str, threshold: float = HIGH_ENTROPY_THRESHOLD) -> bool:
    """Return True when the string exceeds the suspicious entropy threshold."""
    return shannon_entropy(text) > threshold


if __name__ == "__main__":
    test_cases = [
        "hdfcbank",
        "google",
        "xk92mzlogin",
        "a1b2c3d4e5f6",
        "facebook",
    ]
    for domain in test_cases:
        entropy = shannon_entropy(domain)
        flag = "HIGH (suspicious)" if is_high_entropy(domain) else "normal"
        logger.info("%-20s entropy=%6.4f -> %s", domain, entropy, flag)
