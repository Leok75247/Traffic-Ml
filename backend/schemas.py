"""Pydantic models for the public backend API."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.config import DEFAULT_WINDOW_SIZE, FUTURE_STEPS, MIN_OBSERVATIONS, STATE_LABELS


class HealthResponse(BaseModel):
    status: str


class EntitiesResponse(BaseModel):
    entities: list[str]


class DatasetSummaryResponse(BaseModel):
    dataset_label: str
    dataset_source: str
    row_count: int
    entity_count: int
    entities: list[str]
    start_time: datetime
    end_time: datetime
    sampling_interval_seconds: int
    timestamps_reconstructed: bool
    geographic_metadata_available: bool
    available_fields: list[str]
    missing_values_filled: int


class AnalyzeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entity_id: str = Field(min_length=1, max_length=200)
    window_size: int = Field(default=DEFAULT_WINDOW_SIZE, ge=MIN_OBSERVATIONS, le=10000)


class ViterbiObservation(BaseModel):
    timestamp: datetime
    state: str


class FutureState(BaseModel):
    step: int = Field(ge=1, le=FUTURE_STEPS)
    state: str
    state_probabilities: dict[str, float]


class TrainingSummary(BaseModel):
    algorithm: str
    iterations: int
    converged: bool
    log_likelihood_history: list[float]


class AnalyzeResponse(BaseModel):
    entity_id: str
    current_state: str
    next_state: str
    state_probabilities: dict[str, float]
    next_state_probabilities: dict[str, float]
    future_state_sequence: list[FutureState]
    viterbi_sequence: list[ViterbiObservation]
    transition_matrix: list[list[float]]
    forward_log_probability: float
    training: TrainingSummary


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail


STATE_NAMES = STATE_LABELS