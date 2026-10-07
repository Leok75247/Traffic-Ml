from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)


def test_health_entities_and_dataset_summary() -> None:
    health_response = client.get("/health")
    entities_response = client.get("/entities")
    summary_response = client.get("/dataset/summary")

    assert health_response.status_code == 200
    assert health_response.json() == {"status": "ok"}
    assert entities_response.json()["entities"] == [str(index) for index in range(170)]
    summary = summary_response.json()
    assert summary_response.status_code == 200
    assert summary["dataset_label"] == "PeMSD8"
    assert summary["row_count"] == 3_035_520
    assert summary["entity_count"] == 170
    assert summary["available_fields"] == ["timestamp", "entity_id", "flow", "occupancy", "speed"]
    assert summary["sampling_interval_seconds"] == 300
    assert summary["timestamps_reconstructed"] is True
    assert summary["geographic_metadata_available"] is False


def test_analyze_returns_computed_finite_model_results() -> None:
    response = client.post("/analyze", json={"entity_id": "0", "window_size": 24})

    assert response.status_code == 200
    result = response.json()
    assert result["entity_id"] == "0"
    assert result["current_state"] in {"Low Traffic", "Medium Traffic", "High Traffic"}
    assert result["next_state"] in {"Low Traffic", "Medium Traffic", "High Traffic"}
    assert len(result["viterbi_sequence"]) == 24
    assert len(result["future_state_sequence"]) == 3
    assert len(result["transition_matrix"]) == 3
    assert all(abs(sum(row) - 1.0) < 1e-8 for row in result["transition_matrix"])
    assert abs(sum(result["state_probabilities"].values()) - 1.0) < 1e-8
    assert abs(sum(result["next_state_probabilities"].values()) - 1.0) < 1e-8
    assert result["training"]["algorithm"].startswith("Baum-Welch")
    assert result["training"]["iterations"] > 0


def test_api_returns_controlled_errors_for_invalid_requests() -> None:
    missing_entity = client.post("/analyze", json={"entity_id": "unknown", "window_size": 24})
    invalid_window = client.post("/analyze", json={"entity_id": "0", "window_size": 2})

    assert missing_entity.status_code == 404
    assert missing_entity.json()["error"]["code"] == "ENTITY_NOT_FOUND"
    assert invalid_window.status_code == 422
    assert invalid_window.json()["error"]["code"] == "INVALID_REQUEST"
