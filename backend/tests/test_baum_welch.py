import numpy as np

from backend.baum_welch import baum_welch
from backend.hmm_engine import initialize_hmm


def test_baum_welch_returns_finite_history_and_valid_parameters() -> None:
    observations = np.array([
        [72.0, 0.04, 0.02], [68.0, 0.05, 0.03], [70.0, 0.04, 0.02],
        [51.0, 0.10, 0.10], [48.0, 0.12, 0.11], [53.0, 0.09, 0.09],
        [25.0, 0.20, 0.30], [28.0, 0.18, 0.28], [23.0, 0.22, 0.32],
    ] * 3)
    model = initialize_hmm(observations, ("flow", "occupancy", "speed"))

    result = baum_welch(model, observations, max_iterations=12)

    assert 1 <= result.iterations <= 12
    assert len(result.log_likelihood_history) == result.iterations + 1
    assert np.isfinite(result.log_likelihood_history).all()
    assert isinstance(result.converged, bool)
    assert np.isclose(result.model.initial_probabilities.sum(), 1.0)
    assert np.allclose(result.model.transition_matrix.sum(axis=1), 1.0)
    assert np.isfinite(result.model.emission_means).all()
    assert np.isfinite(result.model.emission_variances).all()
    assert np.all(result.model.emission_variances > 0)