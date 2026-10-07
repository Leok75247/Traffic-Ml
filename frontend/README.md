# Ambulance Traffic Intelligence Frontend

React/Vite dashboard for the local FastAPI traffic-state service.

## Run locally

Start the backend from the repository root:

```powershell
python -m uvicorn backend.app:app --reload --port 8000
```

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`. Vite proxies `/api` requests to the backend on port 8000.

## Checks

```powershell
npm run lint
npm run build
```
