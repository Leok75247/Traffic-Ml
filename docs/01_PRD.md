# Product Requirements Document

## Project

**Ambulance Traffic State Prediction Using Hidden Markov Models**

## 1. Product Summary

A local web application that analyzes sequential traffic observations and uses a Hidden Markov Model to infer traffic congestion states and estimate the next likely state.

The emergency-response context makes the output relevant to ambulance operations, while the implementation remains a focused academic ML demonstration.

## 2. Problem Statement

Traffic conditions change over time and are not always directly represented as a single stable label. A sequence of observable traffic measurements can be used to infer an underlying traffic condition.

The project asks:

> Can a Hidden Markov Model represent sequential traffic behavior well enough to infer Low, Medium, and High traffic states and estimate the next likely state?

## 3. Target Users

Primary:

- Student demonstrating the project
- Faculty/examiner evaluating the project

Conceptual future users:

- Emergency fleet operators
- Ambulance coordination teams
- Hospitals

The current implementation is not an operational emergency system.

## 4. Core User Journey

1. Open the application.
2. Load the bundled demonstration dataset or upload a compatible CSV.
3. Select a road/sensor/segment.
4. Select an analysis window if needed.
5. Click Analyze.
6. View the current inferred traffic state.
7. View the next predicted state.
8. View probabilities for Low/Medium/High.
9. Inspect the traffic-state timeline.
10. Inspect the Viterbi sequence.
11. Inspect the transition matrix and model statistics.

## 5. Core Inputs

Minimum useful fields:

- timestamp
- entity identifier such as sensor_id, road_id, or route_id
- traffic observations

Preferred traffic measurements:

- speed
- traffic flow/volume
- occupancy

Travel time may be derived or included when the selected dataset supports it.

## 6. Core Outputs

The system should return:

- selected entity
- latest/current inferred state
- next likely state
- state probability distribution
- Viterbi hidden-state sequence
- transition matrix
- Forward sequence probability/log probability
- Baum-Welch training information
- basic data-quality information

## 7. Product Boundaries

The current product does not:

- choose the best ambulance route
- calculate shortest paths
- navigate a vehicle
- connect to live emergency systems
- communicate with hospitals
- collect personal information
- call paid APIs

## 8. Demo Dataset Strategy

The application should support both:

- a bundled demonstration dataset
- a compatible user-uploaded CSV

The bundled dataset exists primarily to make the demo reliable.

The implementation must remain simple: one analysis workflow, not a complex dataset-management system.

## 9. Success Criteria

A successful demonstration means:

- the application launches reliably
- the selected sequence is processed correctly
- the HMM produces valid probabilities
- Forward works
- Viterbi returns a valid sequence
- Baum-Welch training can run or be represented through the selected trusted HMM implementation
- the next-state output comes from the actual model
- visualizations match the actual data/results
- errors are handled cleanly
- the student can explain the core mathematics and pipeline

## 10. Future Product Concept

A future version could provide traffic-state intelligence as an input to emergency-response systems.

That future concept is separate from the current mini-project and must not be represented as already implemented.
