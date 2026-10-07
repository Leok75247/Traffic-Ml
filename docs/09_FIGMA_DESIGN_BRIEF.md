# Figma Design Brief

## Product

**Ambulance Traffic Intelligence**

Supporting title:

**Ambulance Traffic State Prediction Using Hidden Markov Models**

## Design Direction

Combine:

- emergency-operations seriousness
- light modern analytics
- old-money restraint

Think "established operations console" rather than "AI startup landing page."

## Primary Frame

Desktop dashboard approximately 1440 px wide.

Layout:

1. clean header
2. compact controls row
3. three result cards
4. main timeline
5. probability visualization
6. technical model panels
7. concise explanation

## Suggested Wireframe

```text
┌──────────────────────────────────────────────────────────────┐
│ AMBULANCE TRAFFIC INTELLIGENCE                 MODEL READY ● │
│ HMM-Based Traffic Congestion State Analysis                  │
├──────────────────────────────────────────────────────────────┤
│ Entity  [ Sensor 123 ▼ ]     Window [ 48 ]   [ ANALYZE ]    │
├────────────────┬────────────────┬────────────────────────────┤
│ CURRENT        │ NEXT           │ HIGH-PROBABILITY            │
│ MEDIUM         │ HIGH           │ 57%                         │
├────────────────┴────────────────┴────────────────────────────┤
│ Traffic State Timeline                                        │
│                                                              │
├────────────────────────────────┬─────────────────────────────┤
│ State Probabilities             │ Transition Matrix           │
│                                │                             │
├────────────────────────────────┴─────────────────────────────┤
│ Most Likely State Sequence                                    │
│ Low -> Low -> Medium -> High -> High                         │
├──────────────────────────────────────────────────────────────┤
│ Model Statistics                     Why this result?         │
└──────────────────────────────────────────────────────────────┘
```

## Design Tokens

Use a neutral palette with one restrained accent.

Suggested structure:

- Background
- Surface
- Surface subtle
- Border
- Primary text
- Secondary text
- Accent
- Warning/error

Avoid default Tailwind purple/indigo aesthetic.

## Cards

Cards should:

- use modest radius
- use subtle borders
- have restrained shadows
- avoid gradients
- maintain equal internal padding

## KPI Cards

Do not use giant dashboard tiles.

Each card needs:

- small label
- prominent value
- brief supporting line

## State Styling

Low / Medium / High should be distinguishable but not saturated.

The state card is the visual focus.

## Timeline

Show time chronologically.

Prefer an elegant step/line treatment over an overly colorful categorical chart.

## Transition Matrix

Use a compact matrix with clear row/column labels.

Optional subtle intensity encoding is acceptable.

## Explanation Panel

Keep text concise.

Example structure:

```text
WHY THIS RESULT

Recent observations
↓
Current state distribution
↓
Strongest transition
↓
Next predicted state
```

## Responsive

Desktop-first, but the dashboard should remain usable at tablet width.

## Figma Deliverables

Create:

- Desktop main dashboard
- Desktop loading state
- Desktop empty state
- Desktop error state
- Optional compact responsive frame

Do not design dozens of screens.
