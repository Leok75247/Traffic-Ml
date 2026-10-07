# UI / Design System Specification

## 1. Visual Goal

Create a clean, restrained analytics interface inspired by mature operations software.

The visual character should feel:

- old-money
- understated
- institutional
- precise
- calm
- premium
- practical

Not:

- flashy AI
- neon
- purple-gradient SaaS
- green-heavy admin dashboards
- cyberpunk
- glassmorphism everywhere

## 2. Information Hierarchy

The user should understand the result in this order:

1. Current traffic state
2. Next predicted state
3. Probability distribution
4. Traffic state timeline
5. Viterbi sequence
6. Transition matrix
7. Technical model statistics

## 3. Main Screen

Header:

**AMBULANCE TRAFFIC INTELLIGENCE**

Subtitle:

**HMM-Based Traffic Congestion State Analysis**

Top controls:

- entity selector
- analysis window selector
- Analyze button

Primary cards:

- Current Traffic State
- Next Predicted State
- Highest State Probability

Main visual area:

- traffic state timeline
- state probability chart

Technical area:

- transition matrix
- Viterbi path
- Forward log probability
- Baum-Welch training information

## 4. Layout

Prefer a spacious single-page dashboard.

Desktop:

- centered content
- maximum readable width
- 12-column grid where useful
- consistent card heights
- strong alignment

Do not create a huge sidebar unless Figma testing shows it is necessary.

Mobile:

- stack cards
- preserve chart readability
- keep controls usable

## 5. Typography

Use a professional sans-serif such as Inter or a similarly neutral interface font.

Hierarchy:

- large, restrained page title
- medium section titles
- clear metric values
- small metadata labels

Avoid oversized marketing typography.

## 6. Color System

Use mostly neutrals.

Base:

- warm white / off-white or deep charcoal depending on the final Figma theme

Text:

- near-black or warm white

Borders:

- subtle neutral gray

Accent:

- one restrained emergency/operations accent

Traffic states should be visually distinct but muted.

Avoid making every state a saturated "success" color.

## 7. Components

Required reusable components:

- Header
- DatasetStatus
- EntitySelector
- AnalyzeButton
- StateCard
- ProbabilityPanel
- TrafficTimeline
- ViterbiSequence
- TransitionMatrix
- ModelStats
- ResultExplanation
- LoadingState
- EmptyState
- ErrorState

## 8. Animation

Use animation only for:

- loading
- result appearance
- small state transitions

Avoid:

- bouncing cards
- glowing metrics
- large entrance animations
- decorative motion

## 9. Charts

Charts should be:

- clean
- legible
- minimally decorated
- labeled only where useful

Required:

- traffic state over time
- state probabilities

Optional:

- speed/flow/occupancy trend

## 10. Result Explanation

Include a compact explanation panel:

**Why this state?**

Show a short chain such as:

```text
Recent observations
-> inferred state distribution
-> strongest transition
-> next predicted state
```

This must be generated from actual model outputs.

## 11. States

Design all important UI states before implementation:

- first load
- dataset ready
- analyzing
- analysis complete
- invalid data
- insufficient sequence
- API unavailable

## 12. Map Policy

No map is required.

Do not reserve a large map area in the main UI unless a future design decision explicitly adds one.

A small route/entity identifier is sufficient for the current project.
