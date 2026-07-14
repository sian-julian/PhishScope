"""Brand placement checks for phishing-style domain structures."""

from __future__ import annotations

from urllib.parse import urlparse

import tldextract

try:
    from backend.config import BRAND_MISMATCH_POINTS, logger
    from backend.utils.validators import ensure_scheme, get_hostname, is_valid_ip, normalize_url
except ImportError:  # pragma: no cover - supports `python -m analyzer...` from backend/
    from config import BRAND_MISMATCH_POINTS, logger
    from utils.validators import ensure_scheme, get_hostname, is_valid_ip, normalize_url

_TLD_EXTRACTOR = tldextract.TLDExtract(suffix_list_urls=())


def extract_domain_parts(url: str) -> dict:
    """Break a URL or host into public-suffix-aware domain components."""
    normalized_url = ensure_scheme(normalize_url(url))
    parsed = urlparse(normalized_url)
    host = parsed.hostname or get_hostname(normalized_url)

    if not host:
        return {"subdomain": "", "registered_domain": "", "tld": "", "full_domain": ""}

    if host == "localhost" or is_valid_ip(host):
        return {"subdomain": "", "registered_domain": host, "tld": "", "full_domain": host}

    result = _TLD_EXTRACTOR(host)

    return {
        "subdomain": result.subdomain,
        "registered_domain": result.domain,
        "tld": result.suffix,
        "full_domain": host,
    }


def check_brand_position(url: str, brand_list: list) -> dict:
    """Check whether a known brand appears in a suspicious domain position."""
    parts = extract_domain_parts(url)
    result = {
        "brand_found": None,
        "position": None,
        "is_suspicious": False,
        "risk_points": 0,
    }

    for brand in brand_list:
        brand_lower = brand.lower()
        registered_domain = parts["registered_domain"].lower()
        subdomain = parts["subdomain"].lower()

        if registered_domain == brand_lower:
            result["brand_found"] = brand
            result["position"] = "registered_domain"
            result["is_suspicious"] = False
            return result

        if brand_lower in subdomain:
            result["brand_found"] = brand
            result["position"] = "subdomain"
            result["is_suspicious"] = True
            result["risk_points"] = BRAND_MISMATCH_POINTS
            return result

        if brand_lower in registered_domain and registered_domain != brand_lower:
            result["brand_found"] = brand
            result["position"] = "embedded"
            result["is_suspicious"] = True
            result["risk_points"] = BRAND_MISMATCH_POINTS
            return result

    return result


if __name__ == "__main__":
    brands = ["hdfc", "google", "paypal", "amazon"]

    test_urls = [
        "https://hdfc.com/login",                          # legitimate
        "https://hdfc.secure-verification.xyz/login",      # brand in subdomain
        "https://secure-hdfc-login.com/verify",            # brand embedded
        "https://www.google.com/search",                   # legitimate (www is subdomain, fine)
        "https://accounts.paypal-secure-check.net/",       # brand embedded in fake domain
    ]

    for u in test_urls:
        r = check_brand_position(u, brands)
        logger.info("%-50s -> %s", u, r)
