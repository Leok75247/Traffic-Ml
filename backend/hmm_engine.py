"""Validated diagonal-Gaussian HMM primitives for traffic observations."""

from dataclasses import dataclass

import numpy as np

from backend.config import NUM_STATES, STATE_LABELS, VARIANCE_FLOOR


def _as_finite_array(value: np.ndarray, name: str) -> np.ndarray:
    array = np.asarray(value, dtype=np.float64)
    if not np.isfinite(array).all():
        raise ValueError(f"{name} must contain only finite values.")
    return array


@dataclass
class GaussianHMM:
    """A discrete-state HMM with independent Gaussian emission features."""

    initial_probabilities: np.ndarray
    transition_matrix: np.ndarray
    emission_means: np.ndarray
    emission_variances: np.ndarray
    feature_mean: np.ndarray
    feature_scale: np.ndarray
    feature_names: tuple[str, ...]

    def __post_init__(self) -> None:
        self.initial_probabilities = _as_finite_array(self.initial_probabilities, "initial_probabilities")
        self.transition_matrix = _as_finite_array(self.transition_matrix, "transition_matrix")
        self.emission_means = _as_finite_array(self.emission_means, "emission_means")
        self.emission_variances = _as_finite_array(self.emission_variances, "emission_variances")
        self.feature_mean = _as_finite_array(self.feature_mean, "feature_mean")
        self.feature_scale = _as_finite_array(self.feature_scale, "feature_scale")
        self.feature_names = tuple(self.feature_names)
        self.validate()

    @property
    def n_states(self) -> int:
        return len(STATE_LABELS)

    @property
    def n_features(self) -> int:
        return len(self.feature_names)

    def validate(self) -> None:
        states = NUM_STATES
        features = self.n_features
        if features == 0 or self.initial_probabilities.shape != (states,):
            raise ValueError("The initial distribution or feature shape is invalid.")
        if self.transition_matrix.shape != (states, states):
            raise ValueError("The transition matrix must have one row and column per state.")
        if self.emission_means.shape != (states, features) or self.emission_variances.shape != (states, features):
            raise ValueError("Emission parameter shapes do not match the states and features.")
        if self.feature_mean.shape != (features,) or self.feature_scale.shape != (features,):
            raise ValueError("Feature scaling parameters do not match the features.")
        if np.any(self.initial_probabilities < 0) or not np.isclose(self.initial_probabilities.sum(), 1.0):
            raise ValueError("Initial probabilities must be non-negative and sum to one.")
        if np.any(self.transition_matrix < 0) or not np.allclose(self.transition_matrix.sum(axis=1), 1.0):
            raise ValueError("Transition rows must be non-negative and sum to one.")
        if np.any(self.emission_variances <= 0) or np.any(self.feature_scale <= 0):
            raise ValueError("Emission variances and feature scales must be positive.")

    def standardize(self, observations: np.ndarray) -> np.ndarray:
        values = _as_finite_array(observations, "observations")
        if values.ndim != 2 or values.shape[1] != self.n_features or values.shape[0] == 0:
            raise ValueError("Observations must be a non-empty matrix with the configured feature count.")
        return (values - self.feature_mean) / self.feature_scale

    def log_emission_probabilities(self, observations: np.ndarray) -> np.ndarray:
        """Return log p(observation_t | state) for every time and state."""
        standardized = self.standardize(observations)
        difference = standardized[:, None, :] - self.emission_means[None, :, :]
        terms = np.log(2.0 * np.pi * self.emission_variances)[None, :, :]
        return -0.5 * np.sum(terms + difference**2 / self.emission_variances[None, :, :], axis=2)


def _congestion_score(means: np.ndarray, feature_names: tuple[str, ...]) -> np.ndarray:
    """Score states from speed/occupancy, or flow when those are unavailable."""
    scores = np.zeros(means.shape[0], dtype=np.float64)
    contributors = 0
    if "speed" in feature_names:
        scores -= means[:, feature_names.index("speed")]
        contributors += 1
    if "occupancy" in feature_names:
        scores += means[:, feature_names.index("occupancy")]
        contributors += 1
    if contributors == 0 and "flow" in feature_names:
        scores += means[:, feature_names.index("flow")]
        contributors = 1
    if contributors == 0:
        scores += means[:, 0]
        contributors = 1
    return scores / contributors


def initialize_hmm(observations: np.ndarray, feature_names: tuple[str, ...]) -> GaussianHMM:
    """Build reproducible quantile-based emission parameters for three states."""
    values = _as_finite_array(observations, "observations")
    feature_names = tuple(feature_names)
    if values.ndim != 2 or values.shape[1] != len(feature_names) or values.shape[0] < NUM_STATES:
        raise ValueError("At least three observations and matching feature names are required.")
    feature_mean = values.mean(axis=0)
    feature_scale = values.std(axis=0)
    feature_scale[feature_scale < VARIANCE_FLOOR] = 1.0
    standardized = (values - feature_mean) / feature_scale
    order = np.argsort(_congestion_score(standardized, feature_names), kind="stable")
    groups = np.array_split(order, NUM_STATES)
    emission_means = np.vstack([standardized[group].mean(axis=0) for group in groups])
    global_variance = np.maximum(standardized.var(axis=0), VARIANCE_FLOOR)
    emission_variances = np.vstack([
        np.maximum(standardized[group].var(axis=0), VARIANCE_FLOOR) for group in groups
    ])
    emission_variances = np.maximum(emission_variances, global_variance[None, :] * 0.05)
    transition_matrix = np.full((NUM_STATES, NUM_STATES), 0.1 / (NUM_STATES - 1))
    np.fill_diagonal(transition_matrix, 0.9)
    return GaussianHMM(
        initial_probabilities=np.full(NUM_STATES, 1.0 / NUM_STATES),
        transition_matrix=transition_matrix,
        emission_means=emission_means,
        emission_variances=emission_variances,
        feature_mean=feature_mean,
        feature_scale=feature_scale,
        feature_names=feature_names,
    )


def order_states_by_traffic(model: GaussianHMM) -> GaussianHMM:
    """Ensure state indices follow increasing inferred congestion."""
    order = np.argsort(_congestion_score(model.emission_means, model.feature_names), kind="stable")
    return GaussianHMM(
        initial_probabilities=model.initial_probabilities[order],
        transition_matrix=model.transition_matrix[np.ix_(order, order)],
        emission_means=model.emission_means[order],
        emission_variances=model.emission_variances[order],
        feature_mean=model.feature_mean,
        feature_scale=model.feature_scale,
        feature_names=model.feature_names,
    )