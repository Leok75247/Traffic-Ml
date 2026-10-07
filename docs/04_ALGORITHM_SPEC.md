# Algorithm Specification

## 1. Objective

Model traffic as a sequence where the actual congestion condition is represented as a hidden state and traffic measurements are observations.

## 2. Hidden States

Use exactly three semantic states:

```text
0 = Low Traffic
1 = Medium Traffic
2 = High Traffic
```

The UI should use the labels, not numeric codes.

## 3. Observations

Observations may use:

- speed
- flow
- occupancy

The exact emission representation must match the selected HMM type.

## 4. HMM Parameters

Represent:

- initial state probability vector pi
- transition matrix A
- observation/emission parameters B or their continuous equivalent

Required numerical properties:

- probabilities >= 0
- each probability vector/matrix row normalized appropriately
- no silent NaN/inf values

## 5. Forward Algorithm

Purpose:

Calculate the likelihood of an observation sequence under the HMM.

Responsibilities:

- initialize
- recurse
- terminate
- return stable likelihood/log-likelihood

Prefer log-space calculations or another numerically stable method for longer sequences.

Expose enough intermediate information for a demonstration.

## 6. Viterbi Algorithm

Purpose:

Find the most likely sequence of hidden traffic states.

Responsibilities:

- initialization
- recurrence
- backpointers
- termination
- backtracking

Return one state for each observation.

The resulting sequence must use the semantic labels:

```text
Low -> Medium -> High
```

## 7. Baum-Welch / Forward-Backward

Purpose:

Estimate or refine HMM parameters using the observation sequences.

Implementation strategy:

- use a mature HMM library where it reduces numerical risk
- make the mapping between library training and Baum-Welch/EM explicit
- record convergence/log-likelihood information

If a hand-written implementation is used for educational visibility, test it against the trusted library on a small controlled example.

## 8. Library Strategy

Preferred philosophy:

**trusted numerical implementation + transparent project-level wrappers + tests**

Use `hmmlearn` only as a reference/validation implementation if it fits the selected environment. Its current PyPI release is 0.3.3, but the project is explicitly marked as being in limited-maintenance mode, so do not build the whole project around undocumented internals or assume future API stability.

The project should expose its own tested functions for the concepts that matter in the demonstration. Library output is a cross-check, not a substitute for understanding the mathematics.

For example, a mature HMM library may be used as a reference implementation while project code exposes:

- model parameters
- Forward result
- Viterbi path
- training history

## 9. Next-State Estimation

The system should estimate the next state from the current state distribution and transition probabilities.

The result must be derived from the model.

Do not simply choose a state from a hardcoded rule.

## 10. Numerical Testing

Test:

- probability normalization
- known toy HMM
- short observation sequences
- one-observation edge case
- longer sequences
- missing/invalid inputs
- reproducibility with fixed seed

## 11. Interpretation

Example interpretation:

> The recent observation sequence produces the highest posterior/transition-supported probability for High Traffic, so the system reports High as the next most likely state.

The UI must avoid language that implies certainty.
