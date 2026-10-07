# Ambulance Traffic State Prediction Using Hidden Markov Models

The backend analyzes the verified PeMSD8 traffic tensor using a three-state Gaussian Hidden Markov Model. The current implementation is backend-only; the frontend is not part of this phase.

## Run the backend

From the repository root:

```powershell
python -m uvicorn backend.app:app --reload
```

The API is available at `http://127.0.0.1:8000`. Its bundled dataset is `data/raw/pems08.npz`; see [the dataset decision](docs/DATASET_DECISION.md) for verified channel semantics and timestamp reconstruction.

Inspect the actual NPZ file with:

```powershell
python -m backend.dataset_adapter
```

Run backend tests with:

```powershell
python -m pytest backend/tests -q
```
