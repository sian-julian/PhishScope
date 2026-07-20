"""Create reproducible train and test splits from the feature matrix."""

from __future__ import annotations

import sys
from pathlib import Path
from time import perf_counter
from typing import Any

from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from datasets.scripts.common import FEATURE_MATRIX_PATH, TEST_PATH, TRAIN_PATH, add_benchmark, logger, read_csv, save_csv

DEFAULT_TEST_SIZE = 0.2
DEFAULT_RANDOM_STATE = 42


def split_dataset(
    input_path: Path = FEATURE_MATRIX_PATH,
    train_path: Path = TRAIN_PATH,
    test_path: Path = TEST_PATH,
    test_size: float = DEFAULT_TEST_SIZE,
    random_state: int = DEFAULT_RANDOM_STATE,
    benchmark: bool = False,
) -> dict[str, Any]:
    """Stratify the feature matrix into training and testing CSV files."""
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1")

    start_time = perf_counter()
    feature_matrix = read_csv(input_path, {"url", "label"})
    label_counts = feature_matrix["label"].value_counts()
    if len(label_counts) != 2 or label_counts.min() < 2:
        raise ValueError("feature matrix must contain at least two rows for each class")

    train, test = train_test_split(
        feature_matrix,
        test_size=test_size,
        random_state=random_state,
        stratify=feature_matrix["label"],
        shuffle=True,
    )
    train = train.reset_index(drop=True)
    test = test.reset_index(drop=True)
    save_csv(train, train_path)
    save_csv(test, test_path)

    stats: dict[str, Any] = {
        "input_rows": len(feature_matrix),
        "train_rows": len(train),
        "test_rows": len(test),
        "train_path": train_path,
        "test_path": test_path,
    }
    logger.info("Created train/test split: %d train rows, %d test rows", len(train), len(test))
    return add_benchmark(stats, benchmark, start_time)


if __name__ == "__main__":
    logger.info("Dataset splitting completed: %s", split_dataset(benchmark=True))
