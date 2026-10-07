# AI Execution Plan

## Phase 0 — Repository Setup

- create repository structure
- add documentation
- configure backend and frontend
- create minimal test setup

Do not build UI polish yet.

## Phase 1 — Dataset Inspection

- acquire candidate public dataset
- inspect raw format
- document actual schema
- test sequence suitability
- decide final normalized data model

Gate:

Do not continue until the dataset is demonstrably usable.

## Phase 2 — Preprocessing

Implement:

- validation
- timestamp parsing
- ordering
- missing handling
- entity selection
- sequence construction

Create tests.

## Phase 3 — HMM Engine

Implement/integrate:

- state definitions
- HMM parameters
- emission representation
- training

Create deterministic toy examples.

## Phase 4 — Forward

Implement and test the Forward computation.

Cross-check against a trusted HMM implementation where practical.

## Phase 5 — Viterbi

Implement and test Viterbi.

Verify returned path length and validity.

## Phase 6 — Baum-Welch / Forward-Backward

Implement/integrate parameter training.

Record convergence information.

## Phase 7 — Backend API

Add:

- health
- dataset summary
- entities
- analyze

Test API responses.

## Phase 8 — Figma

Create the final visual design using the UI specification.

Design states for:

- initial
- loading
- success
- error

## Phase 9 — Frontend

Implement the Figma design.

Use real API data only.

No hardcoded demo metrics in production UI code.

## Phase 10 — Integration

Connect:

React -> FastAPI -> HMM engine

Validate every displayed number.

## Phase 11 — Visual QA

Compare implementation against Figma.

Fix:

- spacing
- alignment
- typography
- hierarchy
- chart sizing
- responsive layout
- empty/error states

## Phase 12 — Final QA

Run:

- unit tests
- API tests
- integration test
- manual demo

Then prepare:

- README
- report
- presentation
- viva questions
