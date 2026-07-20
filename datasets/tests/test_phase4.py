"""Phase 4 dataset preparation pipeline tests."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

import datasets.scripts.build_features as build_features_module
from datasets.scripts.balance import balance_dataset
from datasets.scripts.build_features import build_feature_matrix
from datasets.scripts.clean import clean_datasets
from datasets.scripts.split import split_dataset


def _write_csv(path: Path, rows: list[dict[str, object]]) -> Path:
    """Write a small CSV fixture and return its path."""
    pd.DataFrame(rows).to_csv(path, index=False)
    return path


def _raw_inputs(tmp_path: Path) -> tuple[Path, Path]:
    """Create representative raw phishing and legitimate URL CSV fixtures."""
    phishing_path = _write_csv(
        tmp_path / "phishing.csv",
        [
            {"url": "HTTPS://PAYPAL-LOGIN.XYZ"},
            {"url": "https://g00gle.xyz"},
            {"url": "...."},
            {"url": None},
            {"url": "https://paypal-login.xyz"},
        ],
    )
    legitimate_path = _write_csv(
        tmp_path / "legitimate_urls.csv",
        [
            {"url": "https://google.com"},
            {"url": "https://cloudflare.com"},
            {"url": " https://GOOGLE.com\n"},
            {"url": ""},
        ],
    )
    return phishing_path, legitimate_path


def test_cleaning_creates_expected_columns_and_labels(tmp_path: Path) -> None:
    phishing_path, legitimate_path = _raw_inputs(tmp_path)
    output_path = tmp_path / "cleaned.csv"
    stats = clean_datasets(phishing_path, legitimate_path, output_path)
    cleaned = pd.read_csv(output_path)
    assert list(cleaned.columns) == ["url", "label", "source"]
    assert set(cleaned["label"]) == {0, 1}
    assert set(cleaned["source"]) == {"phishing", "legitimate"}
    assert stats["cleaned_rows"] == len(cleaned)


def test_cleaning_normalizes_urls(tmp_path: Path) -> None:
    phishing_path, legitimate_path = _raw_inputs(tmp_path)
    output_path = tmp_path / "cleaned.csv"
    clean_datasets(phishing_path, legitimate_path, output_path)
    cleaned = pd.read_csv(output_path)
    assert "https://paypal-login.xyz" in cleaned["url"].tolist()
    assert "https://google.com" in cleaned["url"].tolist()


def test_cleaning_removes_normalized_duplicates(tmp_path: Path) -> None:
    phishing_path, legitimate_path = _raw_inputs(tmp_path)
    output_path = tmp_path / "cleaned.csv"
    stats = clean_datasets(phishing_path, legitimate_path, output_path)
    cleaned = pd.read_csv(output_path)
    assert cleaned["url"].is_unique
    assert stats["duplicates_removed"] == 2


def test_cleaning_removes_null_and_invalid_rows(tmp_path: Path) -> None:
    phishing_path, legitimate_path = _raw_inputs(tmp_path)
    stats = clean_datasets(phishing_path, legitimate_path, tmp_path / "cleaned.csv")
    assert stats["null_rows_removed"] == 2
    assert stats["invalid_rows_removed"] == 1


def test_cleaning_supports_benchmarking(tmp_path: Path) -> None:
    phishing_path, legitimate_path = _raw_inputs(tmp_path)
    stats = clean_datasets(phishing_path, legitimate_path, tmp_path / "cleaned.csv", benchmark=True)
    assert stats["execution_time_ms"] >= 0


def test_cleaning_rejects_missing_file(tmp_path: Path) -> None:
    legitimate_path = _write_csv(tmp_path / "legitimate.csv", [{"url": "https://google.com"}])
    with pytest.raises(FileNotFoundError):
        clean_datasets(tmp_path / "missing.csv", legitimate_path, tmp_path / "cleaned.csv")


def test_cleaning_rejects_missing_url_column(tmp_path: Path) -> None:
    phishing_path = _write_csv(tmp_path / "phishing.csv", [{"domain": "https://bad.xyz"}])
    legitimate_path = _write_csv(tmp_path / "legitimate.csv", [{"url": "https://google.com"}])
    with pytest.raises(ValueError, match="required columns"):
        clean_datasets(phishing_path, legitimate_path, tmp_path / "cleaned.csv")


def test_cleaning_rejects_empty_dataset(tmp_path: Path) -> None:
    phishing_path = tmp_path / "phishing.csv"
    phishing_path.write_text("url\n", encoding="ascii")
    legitimate_path = _write_csv(tmp_path / "legitimate.csv", [{"url": "https://google.com"}])
    with pytest.raises(ValueError, match="empty"):
        clean_datasets(phishing_path, legitimate_path, tmp_path / "cleaned.csv")


def test_balancing_creates_equal_class_counts(tmp_path: Path) -> None:
    input_path = _write_csv(
        tmp_path / "cleaned.csv",
        [{"url": f"https://p{i}.xyz", "label": 1, "source": "phishing"} for i in range(5)]
        + [{"url": f"https://l{i}.com", "label": 0, "source": "legitimate"} for i in range(3)],
    )
    output_path = tmp_path / "balanced.csv"
    stats = balance_dataset(input_path, output_path)
    balanced = pd.read_csv(output_path)
    assert balanced["label"].value_counts().to_dict() == {1: 3, 0: 3}
    assert stats["balanced_rows"] == 6


def test_balancing_respects_requested_target(tmp_path: Path) -> None:
    input_path = _write_csv(
        tmp_path / "cleaned.csv",
        [{"url": f"https://p{i}.xyz", "label": 1, "source": "phishing"} for i in range(5)]
        + [{"url": f"https://l{i}.com", "label": 0, "source": "legitimate"} for i in range(5)],
    )
    stats = balance_dataset(input_path, tmp_path / "balanced.csv", target_per_class=4)
    assert stats["rows_per_class"] == 4
    assert stats["balanced_rows"] == 8


def test_balancing_is_reproducible(tmp_path: Path) -> None:
    input_path = _write_csv(
        tmp_path / "cleaned.csv",
        [{"url": f"https://p{i}.xyz", "label": 1, "source": "phishing"} for i in range(5)]
        + [{"url": f"https://l{i}.com", "label": 0, "source": "legitimate"} for i in range(5)],
    )
    first_path = tmp_path / "first.csv"
    second_path = tmp_path / "second.csv"
    balance_dataset(input_path, first_path, target_per_class=4, random_state=7)
    balance_dataset(input_path, second_path, target_per_class=4, random_state=7)
    assert pd.read_csv(first_path).equals(pd.read_csv(second_path))


def test_balancing_rejects_single_class_data(tmp_path: Path) -> None:
    input_path = _write_csv(
        tmp_path / "cleaned.csv",
        [{"url": "https://only.xyz", "label": 1, "source": "phishing"}],
    )
    with pytest.raises(ValueError, match="both phishing"):
        balance_dataset(input_path, tmp_path / "balanced.csv")


def test_balancing_rejects_invalid_labels(tmp_path: Path) -> None:
    input_path = _write_csv(
        tmp_path / "cleaned.csv",
        [{"url": "https://bad.xyz", "label": 2, "source": "phishing"}],
    )
    with pytest.raises(ValueError, match="only 0 and 1"):
        balance_dataset(input_path, tmp_path / "balanced.csv")


def test_balancing_supports_benchmarking(tmp_path: Path) -> None:
    input_path = _write_csv(
        tmp_path / "cleaned.csv",
        [{"url": f"https://p{i}.xyz", "label": 1, "source": "phishing"} for i in range(2)]
        + [{"url": f"https://l{i}.com", "label": 0, "source": "legitimate"} for i in range(2)],
    )
    stats = balance_dataset(input_path, tmp_path / "balanced.csv", benchmark=True)
    assert stats["execution_time_ms"] >= 0


def test_feature_matrix_has_ml_ready_columns(tmp_path: Path) -> None:
    input_path = _write_csv(
        tmp_path / "balanced.csv",
        [
            {"url": "https://google.com", "label": 0, "source": "legitimate"},
            {"url": "https://g00gle.xyz", "label": 1, "source": "phishing"},
        ],
    )
    output_path = tmp_path / "feature_matrix.csv"
    stats = build_feature_matrix(input_path, output_path, show_progress=False)
    matrix = pd.read_csv(output_path)
    assert len(matrix.columns) >= 20
    assert {"url", "entropy", "tld_score", "lookalike", "label"}.issubset(matrix.columns)
    assert stats["feature_rows"] == 2


def test_feature_matrix_skips_invalid_rows(tmp_path: Path) -> None:
    input_path = _write_csv(
        tmp_path / "balanced.csv",
        [
            {"url": "https://google.com", "label": 0, "source": "legitimate"},
            {"url": "....", "label": 1, "source": "phishing"},
        ],
    )
    stats = build_feature_matrix(input_path, tmp_path / "feature_matrix.csv", show_progress=False)
    assert stats["feature_rows"] == 1
    assert stats["invalid_rows_skipped"] == 1


def test_feature_matrix_skips_extraction_failures(tmp_path: Path, monkeypatch) -> None:
    input_path = _write_csv(
        tmp_path / "balanced.csv",
        [{"url": "https://google.com", "label": 0, "source": "legitimate"}],
    )

    def raise_error(_: str, benchmark: bool = False) -> dict:
        raise RuntimeError("simulated extraction failure")

    monkeypatch.setattr(build_features_module, "extract_features", raise_error)
    stats = build_features_module.build_feature_matrix(input_path, tmp_path / "feature_matrix.csv", show_progress=False)
    assert stats["feature_rows"] == 0
    assert stats["feature_extraction_failures"] == 1


def test_feature_matrix_supports_benchmarking(tmp_path: Path) -> None:
    input_path = _write_csv(
        tmp_path / "balanced.csv",
        [{"url": "https://google.com", "label": 0, "source": "legitimate"}],
    )
    stats = build_feature_matrix(input_path, tmp_path / "feature_matrix.csv", benchmark=True, show_progress=False)
    assert stats["execution_time_ms"] >= 0


def test_split_creates_stratified_train_and_test_files(tmp_path: Path) -> None:
    input_path = _write_csv(
        tmp_path / "feature_matrix.csv",
        [{"url": f"https://p{i}.xyz", "label": 1, "entropy": 3.0} for i in range(10)]
        + [{"url": f"https://l{i}.com", "label": 0, "entropy": 1.0} for i in range(10)],
    )
    train_path = tmp_path / "train.csv"
    test_path = tmp_path / "test.csv"
    stats = split_dataset(input_path, train_path, test_path)
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    assert stats["train_rows"] == 16
    assert stats["test_rows"] == 4
    assert set(train["label"]) == set(test["label"]) == {0, 1}


def test_split_preserves_feature_columns(tmp_path: Path) -> None:
    input_path = _write_csv(
        tmp_path / "feature_matrix.csv",
        [{"url": f"https://p{i}.xyz", "label": 1, "entropy": 3.0, "lookalike": 1} for i in range(5)]
        + [{"url": f"https://l{i}.com", "label": 0, "entropy": 1.0, "lookalike": 0} for i in range(5)],
    )
    train_path = tmp_path / "train.csv"
    test_path = tmp_path / "test.csv"
    split_dataset(input_path, train_path, test_path, test_size=0.4)
    assert list(pd.read_csv(train_path).columns) == list(pd.read_csv(input_path).columns)
    assert list(pd.read_csv(test_path).columns) == list(pd.read_csv(input_path).columns)


def test_split_rejects_missing_label_column(tmp_path: Path) -> None:
    input_path = _write_csv(tmp_path / "feature_matrix.csv", [{"url": "https://google.com"}])
    with pytest.raises(ValueError, match="required columns"):
        split_dataset(input_path, tmp_path / "train.csv", tmp_path / "test.csv")


def test_split_rejects_insufficient_class_rows(tmp_path: Path) -> None:
    input_path = _write_csv(
        tmp_path / "feature_matrix.csv",
        [
            {"url": "https://p.xyz", "label": 1},
            {"url": "https://l1.com", "label": 0},
            {"url": "https://l2.com", "label": 0},
        ],
    )
    with pytest.raises(ValueError, match="at least two"):
        split_dataset(input_path, tmp_path / "train.csv", tmp_path / "test.csv")


def test_split_supports_benchmarking(tmp_path: Path) -> None:
    input_path = _write_csv(
        tmp_path / "feature_matrix.csv",
        [{"url": f"https://p{i}.xyz", "label": 1} for i in range(5)]
        + [{"url": f"https://l{i}.com", "label": 0} for i in range(5)],
    )
    stats = split_dataset(input_path, tmp_path / "train.csv", tmp_path / "test.csv", benchmark=True)
    assert stats["execution_time_ms"] >= 0


def test_full_pipeline_generates_all_outputs(tmp_path: Path) -> None:
    phishing_path = _write_csv(
        tmp_path / "phishing.csv",
        [{"url": f"https://paypa{i}-login.xyz"} for i in range(5)],
    )
    legitimate_path = _write_csv(
        tmp_path / "legitimate.csv",
        [{"url": f"https://example{i}.com"} for i in range(5)],
    )
    cleaned_path = tmp_path / "processed" / "cleaned.csv"
    balanced_path = tmp_path / "processed" / "balanced.csv"
    matrix_path = tmp_path / "features" / "feature_matrix.csv"
    train_path = tmp_path / "splits" / "train.csv"
    test_path = tmp_path / "splits" / "test.csv"

    clean_datasets(phishing_path, legitimate_path, cleaned_path)
    balance_dataset(cleaned_path, balanced_path)
    build_feature_matrix(balanced_path, matrix_path, show_progress=False)
    split_dataset(matrix_path, train_path, test_path, test_size=0.4)

    assert all(path.is_file() for path in (cleaned_path, balanced_path, matrix_path, train_path, test_path))
