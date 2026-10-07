"""Viterbi decoding for GaussianHMM."""

import numpy as np

from backend.forward import logsumexp
from backend.hmm_engine import GaussianHMM


def viterbi(model: GaussianHMM, observations: np.ndarray) -> list[int]:
    """Return the most likely hidden state index for each observation."""
    emissions = model.log_emission_probabilities(observations)
    with np.errstate(divide="ignore"):
        log_initial = np.log(model.initial_probabilities)
        log_transition = np.log(model.transition_matrix)
    scores = np.empty_like(emissions)
    backpointers = np.zeros(emissions.shape, dtype=np.int64)
    scores[0] = log_initial + emissions[0]
    for time_index in range(1, emissions.shape[0]):
        candidates = scores[time_index - 1][:, None] + log_transition
        backpointers[time_index] = np.argmax(candidates, axis=0)
        scores[time_index] = emissions[time_index] + np.max(candidates, axis=0)
    if not np.isfinite(logsumexp(scores[-1])):
        raise ValueError("The model assigns zero probability to the observation sequence.")
    path = np.empty(emissions.shape[0], dtype=np.int64)
    path[-1] = int(np.argmax(scores[-1]))
    for time_index in range(path.size - 2, -1, -1):
        path[time_index] = backpointers[time_index + 1, path[time_index + 1]]
    return path.tolist()