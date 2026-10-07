import numpy as np
import pytest

from backend.dataset_adapter import (
    CHANNEL_INDICES,
    PEMS08_INTERVAL,
    PEMS08_SHAPE,
    DatasetLoadError,
    load_pems08,
    pems08_from_array,
)


def test_real_pems08_file_loads_with_verified_shape_and_time_index() -> None:
    dataset = load_pems08()

    assert dataset.observations.shape == PEMS08_SHAPE
    assert dataset.entity_ids[0] == "0"
    assert dataset.entity_ids[-1] == "169"
    assert dataset.feature_columns == ("flow", "occupancy", "speed")
    assert dataset.timestamps[0].isoformat() == "2016-07-01T00:00:00+00:00"
    assert dataset.timestamps.freqstr == PEMS08_INTERVAL
    assert dataset.row_count == 3_035_520
    assert np.isfinite(dataset.observations).all()


def test_channel_indices_match_verified_source_order() -> None:
    assert CHANNEL_INDICES == {"flow": 0, "occupancy": 1, "speed": 2}


@pytest.mark.parametrize(
    "values, expected_shape, message",
    [
        (np.ones((4, 2)), None, "shape"),
        (np.ones((4, 2, 2)), None, "shape"),
        (np.ones((4, 2, 3)), (4, 3, 3), "expected"),
        (np.full((4, 2, 3), np.nan), None, "NaN or infinite"),
        (np.full((4, 2, 3), np.inf), None, "NaN or infinite"),
    ],
)
def test_invalid_pems08_arrays_fail_cleanly(
    values: np.ndarray,
    expected_shape: tuple[int, int, int] | None,
    message: str,
) -> None:
    with pytest.raises(DatasetLoadError, match=message):
        pems08_from_array(values, expected_shape=expected_shape)