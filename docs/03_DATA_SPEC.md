# Data Specification

## 1. Verified Primary Dataset

The current backend uses the actual `data/raw/pems08.npz` archive. Its observed shape is `(17856, 170, 3)`, dtype is `float64`, and it contains no NaN or infinite values. See `DATASET_DECISION.md` for source provenance and the evidence-backed channel/timestamp mapping.

## 2. Raw-to-Application Data Model

Preferred normalized application fields:

| Field | Type | Meaning |
|---|---|---|
| timestamp | datetime | Time of observation |
| entity_id | string/int | Sensor/road segment identifier |
| speed | float | Average traffic speed |
| flow | float | Traffic flow/volume measurement |
| occupancy | float | Road occupancy measurement |

Do not force fields that the selected dataset does not provide.

## 3. Entity Definition

The application should use a neutral term such as `entity_id` internally.

Depending on the dataset, this may represent:

- sensor
- road segment
- station

Do not call a sensor a "route" unless the dataset actually defines routes.

## 4. Sequence Requirements

For an HMM demonstration, the selected entity must have repeated chronological observations.

At minimum:

- observations must be sortable by time
- sequence length must be sufficient for the chosen training/inference window
- duplicate timestamps should be detected
- large time gaps should be identified

## 5. Preprocessing

1. Load and validate the NPZ `data` tensor.
2. Interpret its verified dimensions as timestep, sensor, and channel.
3. Map channel indices to flow, occupancy, and speed using the documented converter order.
4. Reconstruct UTC timestamps at the verified five-minute interval.
5. Select a sensor index and extract a chronological window without materializing a long-form dataframe.
6. Transform observations using the selected window's feature means and scales.

## 6. Traffic State Representation

Hidden states:

- Low Traffic
- Medium Traffic
- High Traffic

The method for linking observations to these latent states must be documented.

Do not invent fixed thresholds before inspecting the dataset.

Preferred approach:

- derive thresholds or emission distributions from the actual training data
- make the procedure deterministic and explainable
- store the thresholds/parameters used for the demo

## 7. Training and Test Separation

Do not leak future observations into model training.

A chronological split is preferred:

```text
earlier observations -> training
later observations   -> evaluation
```

If the dataset has no ground-truth traffic-state labels, report likelihood/convergence and qualitative sequence consistency rather than pretending that unsupervised states have ground-truth accuracy.

## 8. Data Quality Checks

At startup or dataset selection:

- row count
- entity count
- time range
- sampling interval estimate
- missing percentage
- minimum sequence length
- numerical ranges

## 9. Synthetic Fallback

If the public dataset cannot be prepared in time, a small synthetic sequential dataset may be included.

It must be labeled:

**Synthetic Dataset for Demonstration**

Synthetic results must never be presented as real-world validation.

## 10. Privacy

No personal data is required.

Do not upload traffic datasets to external services simply to process them.
