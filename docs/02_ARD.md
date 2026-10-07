# Architecture & Design Document

## 1. Architecture Goal

Build a small, understandable, locally runnable system with clear boundaries between:

- frontend
- backend/API
- preprocessing
- HMM computation
- visualization data

## 2. High-Level Architecture

```text
Browser
  |
  v
React + Vite + Tailwind
  |
  | HTTP/JSON
  v
FastAPI
  |
  +--> Dataset Service / Preprocessing
  |
  +--> HMM Service
         |
         +--> HMM model
         +--> Forward
         +--> Viterbi
         +--> Baum-Welch / Forward-Backward
  |
  v
Structured analysis response
  |
  v
React visualizations
```

## 3. Recommended Repository Structure

```text
ambulance-traffic-hmm/
├── docs/
│   ├── 00_PROJECT_RULES.md
│   ├── 01_PRD.md
│   ├── 02_ARD.md
│   ├── 03_DATA_SPEC.md
│   ├── 04_ALGORITHM_SPEC.md
│   ├── 05_API_SPEC.md
│   ├── 06_UI_SPEC.md
│   ├── 07_TASK_PLAN.md
│   └── 08_TEST_PLAN.md
├── data/
│   ├── raw/
│   └── processed/
├── backend/
│   ├── app.py
│   ├── schemas.py
│   ├── preprocessing.py
│   ├── hmm_engine.py
│   ├── forward.py
│   ├── viterbi.py
│   ├── baum_welch.py
│   └── evaluation.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── charts/
│   │   ├── lib/
│   │   └── App.jsx
│   └── package.json
├── tests/
├── README.md
└── requirements.txt
```

## 4. Backend Responsibilities

### preprocessing.py
- validate dataset
- parse timestamps
- sort observations
- handle missing values
- create sequences
- prepare model inputs

### hmm_engine.py
- manage HMM parameters
- train/load the model
- expose clean model-level operations

### forward.py
- Forward recursion
- stable probability/log-probability calculation
- testable independent functions

### viterbi.py
- Viterbi dynamic programming
- most likely hidden-state sequence
- backtracking

### baum_welch.py
- parameter estimation/training integration
- convergence tracking
- log-likelihood history

### evaluation.py
- validate outputs
- compute legitimate metrics only when ground truth is available
- otherwise report non-label-dependent evidence

## 5. Frontend Responsibilities

The frontend should:

- load/select data
- select entity
- trigger analysis
- display results
- show model information
- display charts
- show loading/error/empty states

The frontend must not calculate the HMM itself.

## 6. Analysis Flow

```text
Dataset
  -> validation
  -> chronological sorting
  -> selected entity
  -> observation sequence
  -> HMM inference/training
  -> Forward
  -> Viterbi
  -> next-state estimation
  -> response object
  -> UI
```

## 7. Reliability

Use deterministic demo settings where practical:

- fixed random seed
- reproducible preprocessing
- controlled HMM initialization
- bounded iterations
- numerical-stability safeguards

Do not hide instability behind arbitrary clipping.

## 8. Error Handling

Backend must return structured errors for:

- invalid file
- missing columns
- insufficient observations
- invalid entity
- NaN/inf values after preprocessing
- failed model fit

Frontend must convert these into concise human-readable messages.

## 9. Non-Goals

No queues, background workers, distributed processing, model registry, cloud object storage, or production observability stack.
