"""Model-driven traffic-state analysis orchestration."""

from backend.baum_welch import baum_welch
from backend.config import FUTURE_STEPS, MAX_TRAINING_ITERATIONS, STATE_LABELS
from backend.forward import filtering_probabilities, forward_log_probability
from backend.hmm_engine import initialize_hmm, order_states_by_traffic
from backend.dataset_adapter import Pems08Dataset
from backend.preprocessing import NormalizedDataset, extract_entity_sequence
from backend.viterbi import viterbi


def analyze_entity(
    dataset: NormalizedDataset | Pems08Dataset,
    entity_id: str,
    window_size: int,
) -> dict[str, object]:
    """Train and analyze a selected entity using only its requested window."""
    observations, timestamps = extract_entity_sequence(dataset, entity_id, window_size)
    initial_model = initialize_hmm(observations, dataset.feature_columns)
    training = baum_welch(initial_model, observations, max_iterations=MAX_TRAINING_ITERATIONS)
    model = order_states_by_traffic(training.model)

    filtered = filtering_probabilities(model, observations)
    current_probabilities = filtered[-1]
    next_probabilities = current_probabilities @ model.transition_matrix
    future_distribution = next_probabilities.copy()
    future_states: list[dict[str, object]] = []
    for step in range(1, FUTURE_STEPS + 1):
        future_states.append({
            "step": step,
            "state": STATE_LABELS[int(future_distribution.argmax())],
            "state_probabilities": {
                label: float(probability)
                for label, probability in zip(STATE_LABELS, future_distribution, strict=True)
            },
        })
        future_distribution = future_distribution @ model.transition_matrix

    decoded_states = viterbi(model, observations)
    return {
        "entity_id": entity_id,
        "current_state": STATE_LABELS[int(current_probabilities.argmax())],
        "next_state": STATE_LABELS[int(next_probabilities.argmax())],
        "state_probabilities": {
            label: float(probability)
            for label, probability in zip(STATE_LABELS, current_probabilities, strict=True)
        },
        "next_state_probabilities": {
            label: float(probability)
            for label, probability in zip(STATE_LABELS, next_probabilities, strict=True)
        },
        "future_state_sequence": future_states,
        "viterbi_sequence": [
            {"timestamp": timestamp, "state": STATE_LABELS[state]}
            for timestamp, state in zip(timestamps, decoded_states, strict=True)
        ],
        "transition_matrix": model.transition_matrix.tolist(),
        "forward_log_probability": forward_log_probability(model, observations),
        "training": {
            "algorithm": "Baum-Welch (Forward-Backward EM) with diagonal Gaussian emissions",
            "iterations": training.iterations,
            "converged": training.converged,
            "log_likelihood_history": list(training.log_likelihood_history),
        },
    }