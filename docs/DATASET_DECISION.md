# Dataset Decision

## Decision Status

**Verified working dataset: PeMSD8** at `data/raw/pems08.npz`.

The archive contains only the `data` key with a `float64` array of shape `(17856, 170, 3)`. It contains no explicit timestamps, sensor metadata, or geographic coordinates. The file itself does not embed its download revision or license.

## Verified Data Contract

The public LibCity PEMS08 converter loads this exact tensor layout and writes channels, in order, as:

1. `traffic_flow` (channel 0)
2. `traffic_occupancy` (channel 1)
3. `traffic_speed` (channel 2)

The file's measured channel ranges corroborate those semantics: channel 0 is `0..1147` with mean `230.681`, channel 1 is `0..0.8955` with mean `0.0650711`, and channel 2 is `3..82.3` with mean `63.763`.

The converter reconstructs time from `2016-07-01T00:00:00Z` at 300-second intervals, ending at `2016-08-31T23:55:00Z`. The sensor dimension is exposed as stable tensor-index IDs `0` through `169`; these are indices, not geographic identities.

The backend retains the normalized observation order `(flow, occupancy, speed)`. It never fabricates geographic information. No missing or infinite values were found in the bundled file.

## Provenance

- Original dataset location referenced by the converter: [ASTGCN PEMS08](https://github.com/Davidham3/ASTGCN/tree/master/data/PEMS08).
- Channel ordering, timestamps, and sampling interval are implemented by the [LibCity PEMS08 converter](https://github.com/LibCity/Bigscity-LibCity-Datasets/blob/master/pemsd8.py).
- LibCity's published dataset table reports 170 sensors, 17,856 five-minute observations, and the July-August 2016 date range.
- The exact revision and license notice corresponding to the local archive are not recorded in the NPZ and remain to be confirmed from its download source.

## Sequence Strategy

Select a tensor-index sensor, take its latest chronological window, standardize features using only that window, and run the three-state diagonal-Gaussian HMM. No geographic map or route semantics are inferred.
