import numpy as np
import pytest

from backend.baum_welch import baum_welch
from backend.config import STATE_LABELS
from backend.hmm_engine import GaussianHMM, initialize_hmm, order_states_by_traffic


def test_hmm_initialization_uses_three_valid_semantic_states() -> None:
    observations = np.array([[70.0, 10.0, 0.05], [65.0, 15.0, 0.1], [30.0, 50.0, 0.5]] * 4)

    model = order_states_by_traffic(initialize_hmm(observations, ("speed", "flow", "occupancy")))

    assert len(STATE_LABELS) == 3
    assert model.initial_probabilities.shape == (3,)
    assert np.isclose(model.initial_probabilities.sum(), 1.0)
    assert np.allclose(model.transition_matrix.sum(axis=1), 1.0)
    assert np.all(model.emission_variances > 0)


def test_baum_welch_trains_and_returns_valid_convergence_metadata() -> None:
    observations = np.array([
        [68.0, 12.0, 0.08], [67.0, 13.0, 0.09], [69.0, 11.0, 0.07],
        [52.0, 28.0, 0.22], [50.0, 30.0, 0.24], [53.0, 29.0, 0.21],
        [31.0, 49.0, 0.48], [29.0, 52.0, 0.52], [32.0, 50.0, 0.47],
    ] * 3)
    model = initialize_hmm(observations, ("speed", "flow", "occupancy"))

    result = baum_welch(model, observations, max_iterations=20)

    assert result.iterations > 0
    assert result.iterations <= 20
    assert len(result.log_likelihood_history) == result.iterations + 1
    assert np.isfinite(result.log_likelihood_history).all()
    assert np.isclose(result.model.initial_probabilities.sum(), 1.0)
    assert np.allclose(result.model.transition_matrix.sum(axis=1), 1.0)
    assert np.all(result.model.emission_variances > 0)
    assert isinstance(result.converged, bool)


def test_hmm_rejects_invalid_probability_parameters() -> None:
    with pytest.raises(ValueError, match="Initial probabilities"):
        GaussianHMM(
            initial_probabilities=np.array([0.2, 0.2, 0.2]),
            transition_matrix=np.full((3, 3), 1.0 / 3.0),
            emission_means=np.zeros((3, 1)),
            emission_variances=np.ones((3, 1)),
            feature_mean=np.zeros(1),
            feature_scale=np.ones(1),
            feature_names=("speed",),
        )
