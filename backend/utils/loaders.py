"""Load runtime configuration data for PhishScope."""

from __future__ import annotations

from pathlib import Path

try:
    from backend.config import BRANDS_FILE, SUSPICIOUS_TLDS_FILE, logger
except ImportError:  # pragma: no cover - supports `python -m analyzer...` from backend/
    from config import BRANDS_FILE, SUSPICIOUS_TLDS_FILE, logger


def read_data_lines(path: Path) -> list[str]:
    """Read non-empty, non-comment lines from a data file."""
    try:
        return [
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
    except FileNotFoundError:
        logger.error("Data file not found: %s", path)
        return []


def load_brands(path: Path = BRANDS_FILE) -> list[str]:
    """Load unique brand names in lowercase while preserving file order."""
    seen: set[str] = set()
    brands: list[str] = []
    for brand in read_data_lines(path):
        normalized = brand.lower()
        if normalized not in seen:
            brands.append(normalized)
            seen.add(normalized)
    return brands


def load_suspicious_tlds(path: Path = SUSPICIOUS_TLDS_FILE) -> dict[str, set[str]]:
    """Load suspicious TLDs grouped by risk level from an INI-like text file."""
    groups: dict[str, set[str]] = {"high": set(), "medium": set()}
    current_group: str | None = None

    for line in read_data_lines(path):
        if line.startswith("[") and line.endswith("]"):
            current_group = line[1:-1].strip().lower()
            groups.setdefault(current_group, set())
            continue

        if current_group is None:
            logger.warning("Ignoring TLD without risk group: %s", line)
            continue

        groups[current_group].add(line.lower().strip("."))

    return groups
