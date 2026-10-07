# API Specification

## 1. Principles

Keep the API small.

The frontend consumes backend results. The frontend does not implement HMM logic.

## 2. Endpoints

### GET /health

Returns service status.

Example:

```json
{
  "status": "ok"
}
```

### GET /dataset/summary

Returns:

- row count
- entity count
- time range
- available fields
- dataset source
- sampling interval
- whether timestamps were reconstructed
- whether geographic metadata exists

### GET /entities

Returns selectable entity identifiers.
For the bundled PEMS08 tensor these are stable sensor-index strings `0` through `169`, not geographic road identifiers.

### POST /analyze

Input:

```json
{
  "entity_id": "123",
  "window_size": 48
}
```

The exact field names may be adjusted after dataset inspection.

Response:

```json
{
  "entity_id": "123",
  "current_state": "Medium Traffic",
  "next_state": "High Traffic",
  "state_probabilities": {
    "Low Traffic": 0.12,
    "Medium Traffic": 0.31,
    "High Traffic": 0.57
  },
  "viterbi_sequence": [
    {
      "timestamp": "2018-01-02T09:00:00",
      "state": "Low Traffic"
    }
  ],
  "transition_matrix": [
    [0.70, 0.25, 0.05],
    [0.10, 0.65, 0.25],
    [0.03, 0.17, 0.80]
  ],
  "forward_log_probability": -124.82,
  "training": {
    "iterations": 18,
    "converged": true
  }
}
```

Numbers above are illustrative schema examples only. The application must display actual computed values.

## 3. Error Contract

Use consistent errors such as:

```json
{
  "error": {
    "code": "INVALID_DATA",
    "message": "The selected sequence does not contain enough valid observations."
  }
}
```

## 4. CORS

Allow the local frontend origin during development.

Do not open unrestricted production CORS unnecessarily.

## 5. Validation

Use Pydantic request/response models.

Reject:

- missing entity_id
- invalid window sizes
- unsupported file formats
- invalid numerical values where relevant

## 6. API Non-Goals

No authentication endpoints, user profiles, payments, external map services, live traffic feeds, or routing endpoints.
