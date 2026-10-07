"""Dataset normalization and ordered traffic observation extraction."""

from dataclasses import dataclass

import numpy as np
import pandas as pd

from backend.config import MIN_OBSERVATIONS
from backend.dataset_adapter import Pems08Dataset

FIELD_ALIASES = {
    "timestamp": ("timestamp", "time", "datetime"),
    "entity_id": ("entity_id", "sensor_id", "road_id", "route_id"),
    "speed": ("speed", "average_speed", "avg_speed"),
    "flow": ("flow", "traffic_flow", "volume"),
    "occupancy": ("occupancy", "occupancy_rate"),
}
NUMERIC_FIELDS = ("speed", "flow", "occupancy")


class DataValidationError(ValueError):
    """Raised when a dataset cannot satisfy the normalized data contract."""


class MissingEntityError(LookupError):
    """Raised when a requested entity is not present in the dataset."""


class InsufficientObservationsError(ValueError):
    """Raised when an entity has fewer usable observations than required."""


@dataclass(frozen=True)
class NormalizedDataset:
    frame: pd.DataFrame
    feature_columns: tuple[str, ...]
    missing_values_filled: int


def normalize_dataset(frame: pd.DataFrame) -> NormalizedDataset:
    """Normalize generic column aliases and prepare chronologically ordered data."""
    if frame.empty:
        raise DataValidationError("The dataset is empty.")
    normalized_names = {str(column).strip().lower(): column for column in frame.columns}
    rename: dict[object, str] = {}
    for normalized_name, aliases in FIELD_ALIASES.items():
        matches = [normalized_names[alias] for alias in aliases if alias in normalized_names]
        if len(matches) > 1:
            raise DataValidationError(f"Multiple columns map to the normalized field '{normalized_name}'.")
        if matches:
            rename[matches[0]] = normalized_name
    result = frame.rename(columns=rename).copy()
    if "timestamp" not in result or "entity_id" not in result:
        raise DataValidationError("Dataset must provide timestamp and entity_id fields.")
    feature_columns = tuple(field for field in NUMERIC_FIELDS if field in result.columns)
    if not feature_columns:
        raise DataValidationError("Dataset must provide at least one of speed, flow, or occupancy.")
    result["timestamp"] = pd.to_datetime(result["timestamp"], errors="coerce", utc=True)
    result["entity_id"] = result["entity_id"].astype("string").str.strip()
    if result["timestamp"].isna().any() or result["entity_id"].isna().any() or (result["entity_id"] == "").any():
        raise DataValidationError("Timestamp and entity_id values must be present and valid.")
    result = result.sort_values(["entity_id", "timestamp"], kind="stable").reset_index(drop=True)
    if result.duplicated(["entity_id", "timestamp"]).any():
        raise DataValidationError("Duplicate timestamps for an entity are not supported.")

    missing_values_filled = 0
    for feature in feature_columns:
        result[feature] = pd.to_numeric(result[feature], errors="coerce")
        if np.isinf(result[feature].to_numpy(dtype=np.float64, na_value=np.nan)).any():
            raise DataValidationError(f"Feature '{feature}' contains an infinite value.")
        missing_values_filled += int(result[feature].isna().sum())
        result[feature] = result.groupby("entity_id", sort=False)[feature].transform(
            lambda values: values.interpolate(limit_direction="both")
        )
        if result[feature].isna().any():
            raise DataValidationError(f"Feature '{feature}' has no valid values for at least one entity.")
    return NormalizedDataset(result, feature_columns, missing_values_filled)


def extract_entity_sequence(
    dataset: NormalizedDataset | Pems08Dataset,
    entity_id: str,
    window_size: int,
    minimum_observations: int = MIN_OBSERVATIONS,
) -> tuple[np.ndarray, list[pd.Timestamp]]:
    """Return the latest requested observations and timestamps for one entity."""
    if window_size < minimum_observations:
        raise InsufficientObservationsError(
            f"window_size must be at least {minimum_observations} observations."
        )
    if isinstance(dataset, Pems08Dataset):
        try:
            entity_index = dataset.entity_ids.index(str(entity_id))
        except ValueError as error:
            raise MissingEntityError(f"Entity '{entity_id}' was not found.") from error
        observation_count = dataset.observations.shape[0]
        if observation_count < window_size:
            raise InsufficientObservationsError(
                f"Entity '{entity_id}' has {observation_count} observations; {window_size} are required."
            )
        selected = dataset.observations[-window_size:, entity_index, :]
        if not np.isfinite(selected).all():
            raise DataValidationError("Selected observations contain invalid numbers.")
        return selected, dataset.timestamps[-window_size:].tolist()

    entity_rows = dataset.frame.loc[dataset.frame["entity_id"] == str(entity_id)]
    if entity_rows.empty:
        raise MissingEntityError(f"Entity '{entity_id}' was not found.")
    if len(entity_rows) < max(window_size, minimum_observations):
        raise InsufficientObservationsError(
            f"Entity '{entity_id}' has {len(entity_rows)} observations; {window_size} are required."
        )
    selected = entity_rows.tail(window_size)
    observations = selected.loc[:, dataset.feature_columns].to_numpy(dtype=np.float64)
    if not np.isfinite(observations).all():
        raise DataValidationError("Selected observations contain invalid numbers.")
    return observations, selected["timestamp"].tolist()