"""Baum-Welch / Forward-Backward training for the project Gaussian HMM."""

from dataclasses import dataclass

import numpy as np

from backend.config import TRAINING_TOLERANCE, VARIANCE_FLOOR
from backend.forward import forward, logsumexp
from backend.hmm_engine import GaussianHMM


@dataclass(frozen=True)
class TrainingResult:
    model: GaussianHMM
    log_likelihood_history: tuple[float, ...]
    iterations: int
    converged: bool


def baum_welch(
    model: GaussianHMM,
    observations: np.ndarray,
    max_iterations: int = 100,
    tolerance: float = TRAINING_TOLERANCE,
) -> TrainingResult:
    """Estimate initial, transition, and diagonal Gaussian emission parameters via EM."""
    values = np.asarray(observations, dtype=np.float64)
    standardized = model.standardize(values)
    if max_iterations < 1 or tolerance <= 0:
        raise ValueError("max_iterations and tolerance must be positive.")
    emissions = model.log_emission_probabilities(values)
    with np.errstate(divide="ignore"):
        log_transition = np.log(model.transition_matrix)
    log_likelihood_history = [forward(model, values).log_probability]
    converged = False

    for iteration in range(1, max_iterations + 1):
        time_count, state_count = emissions.shape
        log_alpha = np.empty_like(emissions)
        log_beta = np.zeros_like(emissions)
        log_alpha[0] = np.log(model.initial_probabilities) + emissions[0]
        for time_index in range(1, time_count):
            log_alpha[time_index] = emissions[time_index] + logsumexp(
                log_alpha[time_index - 1][:, None] + log_transition, axis=0
            )
        likelihood = float(logsumexp(log_alpha[-1]))
        for time_index in range(time_count - 2, -1, -1):
            log_beta[time_index] = logsumexp(
                log_transition + emissions[time_index + 1][None, :] + log_beta[time_index + 1][None, :],
                axis=1,
            )

        log_gamma = log_alpha + log_beta - likelihood
        gamma = np.exp(log_gamma)
        gamma /= gamma.sum(axis=1, keepdims=True)
        initial_probabilities = gamma[0]
        transition_counts = np.zeros((state_count, state_count), dtype=np.float64)
        for time_index in range(time_count - 1):
            log_xi = (
                log_alpha[time_index][:, None]
                + log_transition
                + emissions[time_index + 1][None, :]
                + log_beta[time_index + 1][None, :]
                - likelihood
            )
            xi = np.exp(log_xi)
            xi_sum = xi.sum()
            if xi_sum > 0:
                transition_counts += xi / xi_sum
        transition_totals = transition_counts.sum(axis=1, keepdims=True)
        transition_matrix = np.divide(
            transition_counts,
            transition_totals,
            out=model.transition_matrix.copy(),
            where=transition_totals > 0,
        )

        emission_means = model.emission_means.copy()
        emission_variances = model.emission_variances.copy()
        for state_index in range(state_count):
            state_weights = gamma[:, state_index]
            weight_total = state_weights.sum()
            if weight_total > np.finfo(np.float64).eps:
                state_mean = np.average(standardized, axis=0, weights=state_weights)
                state_variance = np.average((standardized - state_mean) ** 2, axis=0, weights=state_weights)
                emission_means[state_index] = state_mean
                emission_variances[state_index] = np.maximum(state_variance, VARIANCE_FLOOR)

        model = GaussianHMM(
            initial_probabilities=initial_probabilities,
            transition_matrix=transition_matrix,
            emission_means=emission_means,
            emission_variances=emission_variances,
            feature_mean=model.feature_mean,
            feature_scale=model.feature_scale,
            feature_names=model.feature_names,
        )
        emissions = model.log_emission_probabilities(values)
        with np.errstate(divide="ignore"):
            log_transition = np.log(model.transition_matrix)
        current_likelihood = forward(model, values).log_probability
        log_likelihood_history.append(current_likelihood)
        previous_likelihood = log_likelihood_history[-2]
        if abs(current_likelihood - previous_likelihood) <= tolerance * (1.0 + abs(previous_likelihood)):
            converged = True
            break

    return TrainingResult(
        model=model,
        log_likelihood_history=tuple(log_likelihood_history),
        iterations=len(log_likelihood_history) - 1,
        converged=converged,
    )