"""Lookalike, homograph, and punycode spoofing checks."""

from __future__ import annotations

try:
    from backend.config import LOOKALIKE_POINTS, logger
except ImportError:  # pragma: no cover - supports `python -m analyzer...` from backend/
    from config import LOOKALIKE_POINTS, logger

# Common ASCII lookalike substitutions attackers use for known brand keywords
ASCII_SUBSTITUTIONS = {
    "0": "o",
    "1": "l",
    "3": "e",
    "4": "a",
    "5": "s",
    "7": "t",
    "@": "a",
    "$": "s",
    "!": "i",
}

# A representative set of Unicode characters that are visually near-identical
# to common Latin letters (Cyrillic, Greek, and other confusable scripts).
# This is not exhaustive but covers the characters most frequently abused
# in real-world homograph phishing campaigns.
CONFUSABLE_MAP = {
    "а": "a",  # Cyrillic а U+0430
    "е": "e",  # Cyrillic е U+0435
    "о": "o",  # Cyrillic о U+043E
    "р": "p",  # Cyrillic р U+0440
    "с": "c",  # Cyrillic с U+0441
    "у": "y",  # Cyrillic у U+0443
    "х": "x",  # Cyrillic х U+0445
    "і": "i",  # Cyrillic і U+0456
    "ѕ": "s",  # Cyrillic ѕ U+0455
    "ј": "j",  # Cyrillic ј U+0458
    "α": "a",  # Greek alpha
    "ο": "o",  # Greek omicron
    "ρ": "p",  # Greek rho
    "ν": "v",  # Greek nu
}


def normalize_ascii_substitutions(domain: str) -> str:
    """Replace common ASCII lookalike characters with their letter equivalent."""
    normalized = domain.lower()
    for sub_char, real_char in ASCII_SUBSTITUTIONS.items():
        normalized = normalized.replace(sub_char, real_char)
    return normalized


def contains_unicode_confusable(domain: str) -> bool:
    """Return True when the domain contains a known Unicode confusable."""
    return any(char in CONFUSABLE_MAP for char in domain)


def normalize_unicode_confusables(domain: str) -> str:
    """Replace known Unicode confusable characters with Latin equivalents."""
    return "".join(CONFUSABLE_MAP.get(ch, ch) for ch in domain)


def is_punycode_domain(domain: str) -> bool:
    """Return True when any domain label is punycode encoded."""
    return any(label.startswith("xn--") for label in domain.split("."))


def decode_punycode_domain(domain: str) -> str:
    """Decode punycode labels to Unicode where possible."""
    decoded_labels: list[str] = []
    for label in domain.split("."):
        if not label.startswith("xn--"):
            decoded_labels.append(label)
            continue

        try:
            decoded_labels.append(label.encode("ascii").decode("idna"))
        except UnicodeError:
            logger.warning("Failed to decode punycode label: %s", label)
            decoded_labels.append(label)

    return ".".join(decoded_labels)


def _match_brand(candidate: str, domain_lower: str, brand_list: list[str]) -> str | None:
    """Return the first brand that appears after normalization but not directly."""
    for brand in brand_list:
        brand_lower = brand.lower()
        if brand_lower in candidate and brand_lower not in domain_lower:
            return brand_lower
    return None


def check_lookalike(domain: str, brand_list: list[str]) -> dict:
    """Check a domain against known brands for visual spoofing signals."""
    result = {
        "ascii_lookalike_detected": False,
        "unicode_confusable_detected": False,
        "punycode_detected": False,
        "decoded_domain": None,
        "normalized_decoded_domain": None,
        "matched_brand": None,
        "risk_points": 0,
    }

    domain_lower = domain.lower()

    if is_punycode_domain(domain_lower):
        result["punycode_detected"] = True
        result["risk_points"] += LOOKALIKE_POINTS
        decoded_domain = decode_punycode_domain(domain_lower)
        result["decoded_domain"] = decoded_domain
        normalized_decoded = normalize_unicode_confusables(decoded_domain).lower()
        result["normalized_decoded_domain"] = normalized_decoded
        matched_brand = _match_brand(normalized_decoded, domain_lower, brand_list)
        if matched_brand:
            result["unicode_confusable_detected"] = True
            result["matched_brand"] = matched_brand

    if contains_unicode_confusable(domain):
        normalized = normalize_unicode_confusables(domain).lower()
        matched_brand = _match_brand(normalized, domain_lower, brand_list)
        if matched_brand:
            result["unicode_confusable_detected"] = True
            result["matched_brand"] = matched_brand
            result["risk_points"] += LOOKALIKE_POINTS

    normalized_ascii = normalize_ascii_substitutions(domain_lower)
    matched_brand = _match_brand(normalized_ascii, domain_lower, brand_list)
    if matched_brand:
        result["ascii_lookalike_detected"] = True
        if result["matched_brand"] is None:
            result["matched_brand"] = matched_brand
        result["risk_points"] += LOOKALIKE_POINTS

    return result


if __name__ == "__main__":
    brands = ["google", "paypal", "hdfc", "microsoft", "amazon"]

    test_domains = [
        "google.com",              # legitimate, no flag expected
        "g00gle.com",              # ASCII lookalike (0 -> o)
        "paypa1-verify.com",       # ASCII lookalike (1 -> l)
        "xn--pypal-4ve.com",       # punycode-encoded
        "micr0soft-login.net",     # ASCII lookalike
        "amazon.com",              # legitimate
    ]

    for d in test_domains:
        r = check_lookalike(d, brands)
        logger.info("%-25s -> %s", d, r)
