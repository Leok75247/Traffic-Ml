"""PEMS08 NPZ loading and normalization boundary."""

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


PEMS08_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "pems08.npz"
PEMS08_SHAPE = (17856, 170, 3)
PEMS08_START = "2016-07-01T00:00:00Z"
PEMS08_INTERVAL = "5min"
PEMS08_INTERVAL_SECONDS = 300
PEMS08_SOURCE = "ASTGCN PEMS08, normalized using the LibCity PEMS08 converter"
PEMS08_SOURCE_URL = "https://github.com/Davidham3/ASTGCN/tree/master/data/PEMS08"
CHANNEL_INDICES = {"flow": 0, "occupancy": 1, "speed": 2}
FEATURE_COLUMNS = ("flow", "occupancy", "speed")


class DatasetLoadError(ValueError):
    """Raised when the configured PEMS08 archive does not match its contract."""


@dataclass(frozen=True)
class Pems08Dataset:
    """Compact normalized tensor with implicit PEMS08 timestamps reconstructed."""

    observations: np.ndarray
    timestamps: pd.DatetimeIndex
    entity_ids: tuple[str, ...]
    feature_columns: tuple[str, ...] = FEATURE_COLUMNS
    dataset_label: str = "PeMSD8"
    missing_values_filled: int = 0

    @property
    def row_count(self) -> int:
        """Return the number of entity-time records represented by the tensor."""
        return int(self.observations.shape[0] * self.observations.shape[1])

    @property
    def start_time(self) -> pd.Timestamp:
        return self.timestamps[0]

    @property
    def end_time(self) -> pd.Timestamp:
        return self.timestamps[-1]


def pems08_from_array(
    values: np.ndarray,
    *,
    expected_shape: tuple[int, int, int] | None = None,
) -> Pems08Dataset:
    """Validate a time-by-sensor-by-channel array and attach verified semantics."""
    data = np.asarray(values)
    if not np.issubdtype(data.dtype, np.number):
        raise DatasetLoadError("PEMS08 data must contain numeric values.")
    if data.ndim != 3 or data.shape[2] != len(CHANNEL_INDICES):
        raise DatasetLoadError("PEMS08 data must have shape (timesteps, sensors, 3 channels).")
    if data.shape[0] == 0 or data.shape[1] == 0:
        raise DatasetLoadError("PEMS08 data must contain timesteps and sensors.")
    if expected_shape is not None and data.shape != expected_shape:
        raise DatasetLoadError(
            f"PEMS08 data has shape {data.shape}; expected {expected_shape}."
        )
    if not np.isfinite(data).all():
        raise DatasetLoadError("PEMS08 data contains NaN or infinite values.")

    timestamps = pd.date_range(PEMS08_START, periods=data.shape[0], freq=PEMS08_INTERVAL)
    entity_ids = tuple(str(index) for index in range(data.shape[1]))
    return Pems08Dataset(
        observations=data,
        timestamps=timestamps,
        entity_ids=entity_ids,
    )


def load_pems08(path: str | Path = PEMS08_PATH) -> Pems08Dataset:
    """Load and validate the canonical PeMSD8 NPZ file without modifying it."""
    try:
        with np.load(path, allow_pickle=False) as archive:
            if "data" not in archive.files:
                raise DatasetLoadError("PEMS08 archive must contain a 'data' array.")
            if archive.files != ["data"]:
                raise DatasetLoadError("PEMS08 archive must contain only the 'data' array.")
            return pems08_from_array(archive["data"], expected_shape=PEMS08_SHAPE)
    except DatasetLoadError:
        raise
    except (OSError, ValueError, EOFError) as error:
        raise DatasetLoadError("PEMS08 archive could not be read.") from error


def inspect_pems08(path: str | Path = PEMS08_PATH) -> dict[str, object]:
    """Return actual archive metadata and statistics for each verified channel."""
    dataset = load_pems08(path)
    raw = dataset.observations
    channels = {
        name: {
            "index": channel_index,
            "minimum": float(np.min(raw[:, :, channel_index])),
            "mean": float(np.mean(raw[:, :, channel_index])),
            "maximum": float(np.max(raw[:, :, channel_index])),
        }
        for name, channel_index in CHANNEL_INDICES.items()
    }
    return {
        "keys": ["data"],
        "shape": raw.shape,
        "dtype": str(raw.dtype),
        "timesteps": raw.shape[0],
        "sensors": raw.shape[1],
        "channels": raw.shape[2],
        "nan_count": int(np.isnan(raw).sum()),
        "inf_count": int(np.isinf(raw).sum()),
        "has_explicit_timestamps": False,
        "has_geographic_metadata": False,
        "channels_by_semantic": channels,
    }


def main() -> None:
    """Print a reproducible text report for the bundled PEMS08 file."""
    report = inspect_pems08()
    print("DATASET INSPECTION")
    print("------------------")
    print(f"Source: {PEMS08_SOURCE}")
    print(f"Keys: {report['keys']}")
    print(f"Shape: {report['shape']}")
    print(f"Dtype: {report['dtype']}")
    print(f"Timesteps: {report['timesteps']}")
    print(f"Sensors: {report['sensors']}")
    print(f"Channels: {report['channels']}")
    print(f"NaNs: {report['nan_count']}")
    print(f"Infs: {report['inf_count']}")
    print(f"Timestamps explicit: {report['has_explicit_timestamps']}")
    print(f"Geographic metadata in NPZ: {report['has_geographic_metadata']}")
    for name, stats in report["channels_by_semantic"].items():
        print(
            f"{name.title()} (channel {stats['index']}): "
            f"min={stats['minimum']:.6g}, mean={stats['mean']:.6g}, "
            f"max={stats['maximum']:.6g}"
        )


if __name__ == "__main__":
    main()