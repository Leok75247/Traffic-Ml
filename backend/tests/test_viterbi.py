import numpy as np
from hmmlearn.hmm import GaussianHMM as ReferenceGaussianHMM

from backend.hmm_engine import GaussianHMM
from backend.viterbi import viterbi


def test_viterbi_decodes_known_state_sequence() -> None:
    model = GaussianHMM(
        initial_probabilities=np.array([0.98, 0.01, 0.01]),
        transition_matrix=np.array([[0.97, 0.02, 0.01], [0.01, 0.98, 0.01], [0.01, 0.02, 0.97]]),
        emission_means=np.array([[-2.0], [0.0], [2.0]]),
        emission_variances=np.full((3, 1), 0.08),
        feature_mean=np.zeros(1),
        feature_scale=np.ones(1),
        feature_names=("speed",),
    )
    observations = np.array([[-2.1], [-1.9], [0.0], [2.0], [2.1]])

    states = viterbi(model, observations)

    assert states == [0, 0, 1, 2, 2]
    assert len(states) == len(observations)
    assert set(states) <= {0, 1, 2}


def test_viterbi_matches_hmmlearn_reference() -> None:
    model = GaussianHMM(
        initial_probabilities=np.array([0.98, 0.01, 0.01]),
        transition_matrix=np.array([
            [0.97, 0.02, 0.01], [0.01, 0.98, 0.01], [0.01, 0.02, 0.97]
        ]),
        emission_means=np.array([[-2.0], [0.0], [2.0]]),
        emission_variances=np.full((3, 1), 0.08),
        feature_mean=np.zeros(1),
        feature_scale=np.ones(1),
        feature_names=("speed",),
    )
    observations = np.array([[-2.1], [-1.9], [0.0], [2.0], [2.1]])
    reference = ReferenceGaussianHMM(
        n_components=3,
        covariance_type="diag",
        init_params="",
        params="",
    )
    reference.startprob_ = model.initial_probabilities
    reference.transmat_ = model.transition_matrix
    reference.means_ = model.emission_means
    reference.covars_ = model.emission_variances

    _, expected_states = reference.decode(observations, algorithm="viterbi")

    assert viterbi(model, observations) == expected_states.tolist()
