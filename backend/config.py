"""Project-wide configuration for PhishScope."""

from __future__ import annotations

import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

BRANDS_FILE = DATA_DIR / "brands.txt"
SUSPICIOUS_TLDS_FILE = DATA_DIR / "suspicious_tlds.txt"

HIGH_ENTROPY_THRESHOLD = 3.5

IP_RISK_POINTS = 25
LOOKALIKE_POINTS = 15
BRAND_MISMATCH_POINTS = 20

TLD_RISK_POINTS = {
    "high": 15,
    "medium": 7,
    "low": 0,
}

MEDIUM_URL_LENGTH_THRESHOLD = 75
HIGH_URL_LENGTH_THRESHOLD = 120
URL_LENGTH_RISK_POINTS = {
    "high": 10,
    "medium": 5,
    "low": 0,
}

LOGGER_NAME = "phishscope"
LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure and return the project logger."""
    logging.basicConfig(level=level, format=LOG_FORMAT)
    return logging.getLogger(LOGGER_NAME)


logger = configure_logging()
