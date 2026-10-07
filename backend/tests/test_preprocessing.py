import numpy as np
import pandas as pd
import pytest

from backend.dataset_adapter import load_pems08
from backend.preprocessing import (
    DataValidationError,
    InsufficientObservationsError,
    MissingEntityError,
    extract_entity_sequence,
    normalize_dataset,
)


def _dataset() -> pd.DataFrame:
    return pd.DataFrame({
        "datetime": ["2024-01-01T00:10:00Z", "2024-01-01T00:00:00Z", "2024-01-01T00:05:00Z"],
        "sensor_id": ["S1", "S1", "S1"],
        "average_speed": [50.0, 60.0, None],
    })


def test_preprocessing_normalizes_aliases_sorts_and_fills_missing_values() -> None:
    dataset = normalize_dataset(_dataset())

    assert dataset.feature_columns == ("speed",)
    assert dataset.frame["timestamp"].is_monotonic_increasing
    assert dataset.frame["speed"].tolist() == [60.0, 55.0, 50.0]
    assert dataset.missing_values_filled == 1


def test_preprocessing_rejects_missing_contract_fields_and_duplicate_timestamps() -> None:
    with pytest.raises(DataValidationError, match="timestamp and entity_id"):
        normalize_dataset(pd.DataFrame({"speed": [10.0]}))

    duplicate = pd.DataFrame({
        "timestamp": ["2024-01-01", "2024-01-01"],
        "entity_id": ["S1", "S1"],
        "speed": [10.0, 12.0],
    })
    with pytest.raises(DataValidationError, match="Duplicate timestamps"):
        normalize_dataset(duplicate)


def test_preprocessing_rejects_infinite_values_and_short_sequences() -> None:
    invalid = pd.DataFrame({
        "timestamp": ["2024-01-01"], "entity_id": ["S1"], "speed": [float("inf")]
    })
    with pytest.raises(DataValidationError, match="infinite"):
        normalize_dataset(invalid)

    dataset = normalize_dataset(_dataset())
    with pytest.raises(InsufficientObservationsError):
        extract_entity_sequence(dataset, "S1", window_size=6)


def test_pems08_sensor_window_preserves_order_and_verified_timestamps() -> None:
    dataset = load_pems08()

    observations, timestamps = extract_entity_sequence(dataset, "12", window_size=8)

    assert np.array_equal(observations, dataset.observations[-8:, 12, :])
    assert timestamps == dataset.timestamps[-8:].tolist()
    assert observations.shape == (8, 3)
    assert timestamps == sorted(timestamps)


def test_pems08_preprocessing_rejects_unknown_sensor_and_short_window() -> None:
    dataset = load_pems08()

    with pytest.raises(MissingEntityError):
        extract_entity_sequence(dataset, "170", window_size=8)
    with pytest.raises(InsufficientObservationsError):
        extract_entity_sequence(dataset, "0", window_size=len(dataset.timestamps) + 1)
