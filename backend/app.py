"""FastAPI application for the local traffic-state HMM demo."""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from backend.analysis_service import analyze_entity
from backend.config import DATASET_PATH
from backend.dataset_adapter import (
    PEMS08_INTERVAL,
    PEMS08_INTERVAL_SECONDS,
    PEMS08_SOURCE,
    PEMS08_SOURCE_URL,
    DatasetLoadError,
    Pems08Dataset,
    load_pems08,
)
from backend.preprocessing import (
    DataValidationError,
    InsufficientObservationsError,
    MissingEntityError,
)
from backend.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    DatasetSummaryResponse,
    EntitiesResponse,
    ErrorResponse,
    HealthResponse,
)

logger = logging.getLogger(__name__)
app = FastAPI(title="Traffic State HMM API", version="0.1.0")


def _load_dataset() -> Pems08Dataset:
    try:
        return load_pems08(DATASET_PATH)
    except (OSError, DatasetLoadError) as error:
        raise RuntimeError("The configured PEMS08 dataset could not be loaded.") from error


app.state.dataset = _load_dataset()
app.state.analysis_cache = {}


def _error_response(status_code: int, code: str, message: str) -> JSONResponse:
    payload = ErrorResponse(error={"code": code, "message": message})
    return JSONResponse(status_code=status_code, content=payload.model_dump())


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(
    request: Request, error: RequestValidationError
) -> JSONResponse:
    del request, error
    return _error_response(422, "INVALID_REQUEST", "The request fields or values are invalid.")


@app.exception_handler(MissingEntityError)
async def missing_entity_error_handler(request: Request, error: MissingEntityError) -> JSONResponse:
    del request
    return _error_response(404, "ENTITY_NOT_FOUND", str(error))


@app.exception_handler(InsufficientObservationsError)
async def insufficient_observations_error_handler(
    request: Request, error: InsufficientObservationsError
) -> JSONResponse:
    del request
    return _error_response(422, "INSUFFICIENT_OBSERVATIONS", str(error))


@app.exception_handler(DataValidationError)
async def data_validation_error_handler(request: Request, error: DataValidationError) -> JSONResponse:
    del request
    return _error_response(422, "INVALID_DATA", str(error))


@app.exception_handler(Exception)
async def unexpected_error_handler(request: Request, error: Exception) -> JSONResponse:
    logger.exception("Unhandled request failure", exc_info=error)
    return _error_response(500, "MODEL_FAILURE", "Analysis could not be completed.")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/entities", response_model=EntitiesResponse)
def entities() -> EntitiesResponse:
    return EntitiesResponse(entities=list(app.state.dataset.entity_ids))


@app.get("/dataset/summary", response_model=DatasetSummaryResponse)
def dataset_summary() -> DatasetSummaryResponse:
    dataset = app.state.dataset
    return DatasetSummaryResponse(
        dataset_label=dataset.dataset_label,
        dataset_source=f"{PEMS08_SOURCE} ({PEMS08_SOURCE_URL})",
        row_count=dataset.row_count,
        entity_count=len(dataset.entity_ids),
        entities=list(dataset.entity_ids),
        start_time=dataset.start_time.to_pydatetime(),
        end_time=dataset.end_time.to_pydatetime(),
        sampling_interval_seconds=PEMS08_INTERVAL_SECONDS,
        timestamps_reconstructed=True,
        geographic_metadata_available=False,
        available_fields=["timestamp", "entity_id", *dataset.feature_columns],
        missing_values_filled=dataset.missing_values_filled,
    )


@app.post("/analyze", response_model=AnalyzeResponse, responses={
    404: {"model": ErrorResponse},
    422: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
})
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    cache = app.state.analysis_cache
    cache_key = (request.entity_id, request.window_size)
    if cache_key not in cache:
        if len(cache) >= 256:
            cache.pop(next(iter(cache)))
        cache[cache_key] = analyze_entity(
            app.state.dataset,
            request.entity_id,
            request.window_size,
        )
    result = cache[cache_key]
    return AnalyzeResponse(**result)