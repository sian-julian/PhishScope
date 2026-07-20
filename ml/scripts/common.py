"""Common utilities for Machine Learning pipeline."""

import json
import logging
from pathlib import Path
from time import perf_counter
from typing import Any

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASETS_DIR = PROJECT_ROOT / "datasets"
ML_DIR = PROJECT_ROOT / "ml"

TRAIN_PATH = DATASETS_DIR / "splits" / "train.csv"
TEST_PATH = DATASETS_DIR / "splits" / "test.csv"

MODELS_DIR = ML_DIR / "models"
EVALUATION_DIR = ML_DIR / "evaluation"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
EVALUATION_DIR.mkdir(parents=True, exist_ok=True)

# Logger setup
logger = logging.getLogger("phishscope_ml")
if not logger.hasHandlers():
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def add_benchmark(stats: dict[str, Any], benchmark: bool, start_time: float) -> dict[str, Any]:
    """Add execution time to stats if benchmark is True."""
    if benchmark:
        stats["execution_time_ms"] = round((perf_counter() - start_time) * 1000, 4)
    return stats


def save_json(data: dict[str, Any], path: Path) -> None:
    """Save dictionary to a JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    logger.info("Saved JSON to %s", path)
