"""Build an ML-ready feature matrix from the balanced URL dataset."""

from __future__ import annotations

import sys
from pathlib import Path
from time import perf_counter
from typing import Any

from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.analyzer.feature_extractor import extract_features
from datasets.scripts.common import BALANCED_PATH, FEATURE_MATRIX_PATH, add_benchmark, logger, read_csv, save_csv


def _feature_row(url: str, label: int, source: str, features: dict[str, Any]) -> dict[str, Any]:
    """Map extractor output to stable, model-ready feature column names."""
    lookalike = any(
        bool(features.get(key))
        for key in (
            "ascii_lookalike_detected",
            "unicode_confusable_detected",
            "punycode_detected",
        )
    )
    return {
        "url": url,
        "label": int(label),
        "source": source,
        "entropy": features["shannon_entropy"],
        "tld_score": features["tld_risk_points"],
        "tld_risk_level": features["tld_risk_level"],
        "brand_mismatch": int(bool(features["brand_mismatch"])),
        "brand_position": features["brand_position"],
        "lookalike": int(lookalike),
        "ascii_lookalike": int(bool(features["ascii_lookalike_detected"])),
        "unicode_homograph": int(bool(features["unicode_confusable_detected"])),
        "punycode": int(bool(features["punycode_detected"])),
        "ip_address": int(bool(features["has_ip_address"])),
        "url_length": features["url_length"],
        "subdomains": features["subdomain_count"],
        "hyphen_count": features["hyphen_count"],
        "has_at_symbol": int(bool(features["has_at_symbol"])),
        "digit_ratio": features["digit_ratio"],
        "token_count": features["token_count"],
        "dot_count": features["dot_count"],
        "uses_https": int(bool(features["uses_https"])),
        "high_entropy": int(bool(features["high_entropy"])),
        "url_length_risk_points": features["url_length_risk_points"],
        "lookalike_matched_brand": features["lookalike_matched_brand"],
    }


def build_feature_matrix(
    input_path: Path = BALANCED_PATH,
    output_path: Path = FEATURE_MATRIX_PATH,
    benchmark: bool = False,
    show_progress: bool = True,
) -> dict[str, Any]:
    """Extract features for every valid URL and save a feature matrix CSV."""
    start_time = perf_counter()
    balanced = read_csv(input_path, {"url", "label", "source"})
    feature_rows: list[dict[str, Any]] = []
    invalid_rows_skipped = 0
    extraction_failures = 0

    records = balanced.loc[:, ["url", "label", "source"]].itertuples(index=False)
    progress = tqdm(records, total=len(balanced), desc="Extracting features", disable=not show_progress)
    for record in progress:
        try:
            features = extract_features(record.url, benchmark=benchmark)
            if not features.get("valid"):
                invalid_rows_skipped += 1
                logger.warning("Skipping invalid URL during feature generation: %s", record.url)
                continue
            feature_rows.append(_feature_row(record.url, record.label, record.source, features))
        except Exception:
            extraction_failures += 1
            logger.exception("Feature extraction failed for URL: %s", record.url)

    import pandas as pd

    feature_matrix = pd.DataFrame(feature_rows)
    save_csv(feature_matrix, output_path)
    stats: dict[str, Any] = {
        "input_rows": len(balanced),
        "feature_rows": len(feature_matrix),
        "invalid_rows_skipped": invalid_rows_skipped,
        "feature_extraction_failures": extraction_failures,
        "feature_columns": len(feature_matrix.columns),
        "output_path": output_path,
    }
    logger.info("Generated feature_matrix.csv with %d rows", len(feature_matrix))
    return add_benchmark(stats, benchmark, start_time)


if __name__ == "__main__":
    logger.info("Feature generation completed: %s", build_feature_matrix(benchmark=True))
