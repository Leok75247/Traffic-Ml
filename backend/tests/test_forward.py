import numpy as np
from hmmlearn.hmm import GaussianHMM as ReferenceGaussianHMM

from backend.forward import filtering_probabilities, forward, forward_log_probability
from backend.hmm_engine import GaussianHMM


def _uniform_emission_model() -> GaussianHMM:
    return GaussianHMM(
        initial_probabilities=np.array([0.2, 0.3, 0.5]),
        transition_matrix=np.array([[0.8, 0.1, 0.1], [0.2, 0.6, 0.2], [0.1, 0.2, 0.7]]),
        emission_means=np.zeros((3, 1)),
        emission_variances=np.ones((3, 1)),
        feature_mean=np.zeros(1),
        feature_scale=np.ones(1),
        feature_names=("speed",),
    )


def _reference_model(model: GaussianHMM) -> ReferenceGaussianHMM:
    reference = ReferenceGaussianHMM(
        n_components=model.n_states,
        covariance_type="diag",
        init_params="",
        params="",
    )
    reference.startprob_ = model.initial_probabilities
    reference.transmat_ = model.transition_matrix
    reference.means_ = model.emission_means
    reference.covars_ = model.emission_variances
    return reference


def test_forward_matches_hand_computed_toy_likelihood() -> None:
    model = _uniform_emission_model()
    observations = np.zeros((2, 1))

    result = forward(model, observations)

    assert np.isclose(result.log_probability, -np.log(2.0 * np.pi))
    assert np.isclose(forward_log_probability(model, observations), result.log_probability)
    assert np.isfinite(result.log_alpha).all()


def test_forward_filtering_is_normalized_and_stable_for_long_sequences() -> None:
    model = _uniform_emission_model()
    observations = np.zeros((1000, 1))

    probabilities = filtering_probabilities(model, observations)
    log_probability = forward_log_probability(model, observations)

    assert np.allclose(probabilities.sum(axis=1), 1.0)
    assert np.isfinite(log_probability)


def test_forward_log_probability_matches_hmmlearn_reference() -> None:
    model = _uniform_emission_model()
    observations = np.array([[-0.7], [0.0], [0.3], [1.1]])

    actual = forward_log_probability(model, observations)
    expected = _reference_model(model).score(model.standardize(observations))

    assert np.isclose(actual, expected, atol=1e-10)
