# Test Plan

## 1. Testing Philosophy

Test the model independently from the frontend.

The UI is considered correct only when it faithfully presents backend outputs.

## 2. Data Tests

Verify:

- required fields
- timestamp parsing
- chronological ordering
- duplicate timestamps
- missing values
- valid numerical ranges
- sufficient sequence length

## 3. HMM Tests

Verify:

- exactly three semantic states
- valid initial probabilities
- valid transition matrix
- valid emission parameters
- normalization
- reproducibility when deterministic settings are used

## 4. Forward Tests

Use a tiny known HMM and manually check:

- initialization
- recurrence
- final probability/log probability

Test a longer sequence for numerical stability.

## 5. Viterbi Tests

Verify:

- returned sequence length == observation length
- all states are valid
- backtracking works
- toy example matches expected path

## 6. Baum-Welch Tests

Verify:

- model can train
- log likelihood does not behave unexpectedly
- convergence handling works
- maximum iteration limit is respected
- parameters remain valid

## 7. API Tests

Test:

- /health
- /dataset/summary
- /entities
- /analyze

Include invalid entity and insufficient sequence cases.

## 8. Frontend Tests

Verify:

- loading state
- successful analysis
- error handling
- API unavailable state
- chart rendering
- probability formatting
- state labels
- responsive layout

## 9. Integration Test

Given a known dataset and entity:

```text
select entity
-> click Analyze
-> backend returns result
-> current state displayed
-> next state displayed
-> probabilities displayed
-> Viterbi sequence displayed
-> transition matrix displayed
```

## 10. Anti-Hallucination Checks

Search the codebase for:

- hardcoded probabilities
- fake accuracy values
- fake route names
- fabricated metrics
- placeholder data accidentally shown as real output
- unused algorithm claims

## 11. Final Acceptance

The project is ready only when:

- the demo runs from a clean environment
- tests pass
- outputs are traceable to actual model computations
- the student can reproduce the main results
- documentation matches the implementation
