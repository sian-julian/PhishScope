"""Clean and label raw phishing and legitimate URL datasets."""

from __future__ import annotations

import sys
from pathlib import Path
from time import perf_counter
from typing import Any

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.utils.validators import normalize_url, validate_url
from datasets.scripts.common import (
    CLEANED_PATH,
    LEGITIMATE_RAW_PATH,
    PHISHING_RAW_PATH,
    add_benchmark,
    logger,
    read_csv,
    save_csv,
)


def _clean_source(path: Path, label: int, source: str) -> tuple[pd.DataFrame, dict[str, int]]:
    """Normalize and validate URL rows from one labelled CSV source."""
    raw_dataframe = read_csv(path, {"url"})
    cleaned = raw_dataframe.loc[:, ["url"]].copy()
    loaded_rows = len(cleaned)

    null_mask = cleaned["url"].isna()
    cleaned = cleaned.loc[~null_mask].copy()
    cleaned["url"] = cleaned["url"].map(normalize_url)

    empty_mask = cleaned["url"].eq("")
    cleaned = cleaned.loc[~empty_mask].copy()

    valid_mask = cleaned["url"].map(lambda value: validate_url(value).valid)
    invalid_urls = cleaned.loc[~valid_mask, "url"]
    if not invalid_urls.empty:
        examples = invalid_urls.head(5).tolist()
        logger.warning(
            "Skipping %d invalid URLs from %s. Examples: %s",
            len(invalid_urls),
            source,
            examples,
        )
    cleaned = cleaned.loc[valid_mask].copy()
    cleaned["label"] = label
    cleaned["source"] = source

    return cleaned, {
        "loaded_rows": loaded_rows,
        "null_rows_removed": int(null_mask.sum() + empty_mask.sum()),
        "invalid_rows_removed": int((~valid_mask).sum()),
    }


def clean_datasets(
    phishing_path: Path = PHISHING_RAW_PATH,
    legitimate_path: Path = LEGITIMATE_RAW_PATH,
    output_path: Path = CLEANED_PATH,
    benchmark: bool = False,
) -> dict[str, Any]:
    """Clean raw URL datasets, label them, and save a combined CSV.

    URLs are deduplicated after normalization. When datasets contain the same
    URL, the phishing row is retained because it is concatenated first.
    """
    start_time = perf_counter()
    phishing, phishing_stats = _clean_source(phishing_path, 1, "phishing")
    legitimate, legitimate_stats = _clean_source(legitimate_path, 0, "legitimate")

    combined = pd.concat([phishing, legitimate], ignore_index=True)
    rows_before_deduplication = len(combined)
    combined = combined.drop_duplicates(subset=["url"], keep="first").reset_index(drop=True)
    duplicates_removed = rows_before_deduplication - len(combined)
    save_csv(combined, output_path)

    stats: dict[str, Any] = {
        "phishing_loaded": phishing_stats["loaded_rows"],
        "legitimate_loaded": legitimate_stats["loaded_rows"],
        "null_rows_removed": phishing_stats["null_rows_removed"] + legitimate_stats["null_rows_removed"],
        "invalid_rows_removed": phishing_stats["invalid_rows_removed"] + legitimate_stats["invalid_rows_removed"],
        "duplicates_removed": duplicates_removed,
        "cleaned_rows": len(combined),
        "output_path": output_path,
    }
    logger.info("Loaded %d phishing URLs", phishing_stats["loaded_rows"])
    logger.info("Loaded %d legitimate URLs", legitimate_stats["loaded_rows"])
    logger.info("Cleaned %d rows", len(combined))
    return add_benchmark(stats, benchmark, start_time)


if __name__ == "__main__":
    logger.info("Dataset cleaning completed: %s", clean_datasets(benchmark=True))
