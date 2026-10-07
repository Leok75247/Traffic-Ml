"""Numerically stable Forward algorithm for GaussianHMM."""

from dataclasses import dataclass

import numpy as np

from backend.hmm_engine import GaussianHMM


def logsumexp(values: np.ndarray, axis: int | None = None) -> np.ndarray:
    """Compute log(sum(exp(values))) without avoidable overflow or underflow."""
    values = np.asarray(values, dtype=np.float64)
    maximum = np.max(values, axis=axis, keepdims=True)
    finite_maximum = np.where(np.isfinite(maximum), maximum, 0.0)
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        result = finite_maximum + np.log(np.sum(np.exp(values - finite_maximum), axis=axis, keepdims=True))
    result = np.where(np.isfinite(maximum), result, maximum)
    result = np.squeeze(result, axis=axis)
    return result


@dataclass(frozen=True)
class ForwardResult:
    log_alpha: np.ndarray
    log_probability: float


def forward(model: GaussianHMM, observations: np.ndarray) -> ForwardResult:
    """Run initialization, recursion, and termination in log space."""
    emissions = model.log_emission_probabilities(observations)
    with np.errstate(divide="ignore"):
        log_initial = np.log(model.initial_probabilities)
        log_transition = np.log(model.transition_matrix)
    log_alpha = np.empty_like(emissions)
    log_alpha[0] = log_initial + emissions[0]
    for time_index in range(1, emissions.shape[0]):
        log_alpha[time_index] = emissions[time_index] + logsumexp(
            log_alpha[time_index - 1][:, None] + log_transition, axis=0
        )
    return ForwardResult(log_alpha=log_alpha, log_probability=float(logsumexp(log_alpha[-1])))


def forward_log_probability(model: GaussianHMM, observations: np.ndarray) -> float:
    """Return the log likelihood of an observation sequence under the model."""
    return forward(model, observations).log_probability


def filtering_probabilities(model: GaussianHMM, observations: np.ndarray) -> np.ndarray:
    """Return normalized Forward state probabilities at each observation."""
    result = forward(model, observations)
    normalizers = logsumexp(result.log_alpha, axis=1)
    return np.exp(result.log_alpha - normalizers[:, None])