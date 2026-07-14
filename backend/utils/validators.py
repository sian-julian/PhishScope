"""Input normalization, host extraction, and URL validation helpers."""

from __future__ import annotations

from dataclasses import dataclass
import ipaddress
from urllib.parse import urlparse

import tldextract

_TLD_EXTRACTOR = tldextract.TLDExtract(suffix_list_urls=())


@dataclass(frozen=True)
class URLValidationResult:
    """Structured result returned by the URL validator."""

    valid: bool
    reason: str | None
    normalized_url: str
    working_url: str
    host: str
    is_ip_address: bool


def normalize_url(url: str) -> str:
    """Normalize raw user input before analysis."""
    return str(url).strip().lower().translate(str.maketrans("", "", "\t\r\n"))


def ensure_scheme(url: str) -> str:
    """Add an HTTP scheme when users provide a bare hostname."""
    return url if "://" in url else f"http://{url}"


def get_hostname(url: str) -> str:
    """Extract the hostname using urllib's parsed hostname support."""
    parsed = urlparse(url)
    return parsed.hostname or ""


def is_valid_ip(host: str) -> bool:
    """Return True when host is a syntactically valid IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(host)
    except ValueError:
        return False
    return True


def validate_url(url: str) -> URLValidationResult:
    """Validate URL-like input before feature extraction."""
    normalized = normalize_url(url)

    if not normalized:
        return URLValidationResult(False, "Invalid URL", normalized, "", "", False)

    working_url = ensure_scheme(normalized)

    try:
        parsed = urlparse(working_url)
        host = parsed.hostname or ""
    except ValueError:
        return URLValidationResult(False, "Invalid URL", normalized, working_url, "", False)

    if parsed.scheme not in {"http", "https"} or not host:
        return URLValidationResult(False, "Invalid URL", normalized, working_url, host, False)

    if any(char.isspace() for char in host) or host.strip(".") != host or ".." in host:
        return URLValidationResult(False, "Invalid URL", normalized, working_url, host, False)

    if host == "localhost":
        return URLValidationResult(True, None, normalized, working_url, host, False)

    if is_valid_ip(host):
        return URLValidationResult(True, None, normalized, working_url, host, True)

    extracted = _TLD_EXTRACTOR(host)
    if not extracted.domain or not extracted.suffix:
        return URLValidationResult(False, "Invalid URL", normalized, working_url, host, False)

    return URLValidationResult(True, None, normalized, working_url, host, False)
