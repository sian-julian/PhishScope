"""Balance cleaned phishing and legitimate URL datasets."""

from __future__ import annotations

import sys
from pathlib import Path
from time import perf_counter
from typing import Any

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from datasets.scripts.common import BALANCED_PATH, CLEANED_PATH, add_benchmark, logger, read_csv, save_csv

DEFAULT_TARGET_PER_CLASS = 50_000
DEFAULT_RANDOM_STATE = 42


def balance_dataset(
    input_path: Path = CLEANED_PATH,
    output_path: Path = BALANCED_PATH,
    target_per_class: int = DEFAULT_TARGET_PER_CLASS,
    random_state: int = DEFAULT_RANDOM_STATE,
    benchmark: bool = False,
) -> dict[str, Any]:
    """Sample each class equally, shuffle it, and save the balanced CSV."""
    if target_per_class <= 0:
        raise ValueError("target_per_class must be positive")

    start_time = perf_counter()
    cleaned = read_csv(input_path, {"url", "label", "source"})
    if not cleaned["label"].isin([0, 1]).all():
        raise ValueError("cleaned dataset labels must contain only 0 and 1")

    phishing = cleaned.loc[cleaned["label"] == 1]
    legitimate = cleaned.loc[cleaned["label"] == 0]
    if phishing.empty or legitimate.empty:
        raise ValueError("cleaned dataset must contain both phishing and legitimate rows")

    selected_per_class = min(target_per_class, len(phishing), len(legitimate))
    balanced = (
        pd.concat(
            [
                phishing.sample(n=selected_per_class, random_state=random_state),
                legitimate.sample(n=selected_per_class, random_state=random_state),
            ],
            ignore_index=True,
        )
        .sample(frac=1, random_state=random_state)
        .reset_index(drop=True)
    )
    save_csv(balanced, output_path)

    stats: dict[str, Any] = {
        "phishing_available": len(phishing),
        "legitimate_available": len(legitimate),
        "rows_per_class": selected_per_class,
        "balanced_rows": len(balanced),
        "output_path": output_path,
    }
    logger.info("Balanced %d phishing and %d legitimate URLs", selected_per_class, selected_per_class)
    return add_benchmark(stats, benchmark, start_time)


if __name__ == "__main__":
    logger.info("Dataset balancing completed: %s", balance_dataset(benchmark=True))
