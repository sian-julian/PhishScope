"""Shared paths and helpers for the Phase 4 dataset pipeline."""

from __future__ import annotations

import sys
from pathlib import Path
from time import perf_counter
from typing import Any

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.config import logger

DATASETS_DIR = PROJECT_ROOT / "datasets"
RAW_DIR = DATASETS_DIR / "raw"
PROCESSED_DIR = DATASETS_DIR / "processed"
FEATURES_DIR = DATASETS_DIR / "features"
SPLITS_DIR = DATASETS_DIR / "splits"

PHISHING_RAW_PATH = RAW_DIR / "phishing.csv"
LEGITIMATE_RAW_PATH = RAW_DIR / "legitimate_urls.csv"
CLEANED_PATH = PROCESSED_DIR / "cleaned.csv"
BALANCED_PATH = PROCESSED_DIR / "balanced.csv"
FEATURE_MATRIX_PATH = FEATURES_DIR / "feature_matrix.csv"
TRAIN_PATH = SPLITS_DIR / "train.csv"
TEST_PATH = SPLITS_DIR / "test.csv"


def elapsed_ms(start_time: float) -> float:
    """Return elapsed time in milliseconds from a perf_counter value."""
    return round((perf_counter() - start_time) * 1000, 4)


def read_csv(path: Path, required_columns: set[str]) -> pd.DataFrame:
    """Read a non-empty CSV and ensure its required columns are available."""
    if not path.is_file():
        logger.error("Dataset file is missing: %s", path)
        raise FileNotFoundError(f"Dataset file not found: {path}")

    dataframe = pd.read_csv(path, low_memory=False)
    if dataframe.empty:
        logger.error("Dataset file is empty: %s", path)
        raise ValueError(f"Dataset is empty: {path}")

    missing_columns = required_columns.difference(dataframe.columns)
    if missing_columns:
        logger.error("Dataset %s is missing columns: %s", path, sorted(missing_columns))
        raise ValueError(f"Dataset is missing required columns: {sorted(missing_columns)}")

    return dataframe


def save_csv(dataframe: pd.DataFrame, path: Path) -> None:
    """Create parent directories and write a CSV without an index column."""
    path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(path, index=False)
    logger.info("Saved %d rows to %s", len(dataframe), path)


def add_benchmark(stats: dict[str, Any], benchmark: bool, start_time: float) -> dict[str, Any]:
    """Add optional timing data to one pipeline stage's result dictionary."""
    if benchmark:
        stats["execution_time_ms"] = elapsed_ms(start_time)
    return stats
