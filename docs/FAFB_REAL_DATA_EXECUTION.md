# FAFB v783 real-data execution gate

The repository includes compressed FAFB artifacts under `para-validacao/`,
but GitHub Actions does not currently run the full-data T4 simulation.
**Do not claim a real FAFB result from synthetic fixture tests.**

## Reproducible execution on a machine with the dataset

1. Identify exact files (annotations, directed Princeton connections,
   optional column assignment). Confirm they are the FAFB v783 snapshot.
2. Inspect real headers before choosing field mappings:

   `python -m cortex.experiments.fafb_inspect para-validacao/consolidated_cell_types.csv.gz PATH_TO_CONNECTIONS.csv.gz`

3. If the actual headers differ from defaults, pass
   `--cell-type-column` and `--synapse-column` to the pilot runner.
   For other differing ID columns, use `select_t4_pilot` keyword arguments
   or add a CLI flag in a subsequent change.
4. Execute:

   `python -m cortex.experiments.t4_pilot_runner --cell-types PATH_TO_TYPES.csv.gz --connections PATH_TO_CONNECTIONS.csv.gz`

5. Archive the input SHA-256, dataset license and snapshot, observed headers,
   selected root IDs and edge counts, parameters, output JSON and runtime.
6. Reject biological interpretation until cell annotations, connection signs,
   sensory mapping and comparison against experimental T4 responses are verified.

## Current scientific scope

The pilot drives all L1 neurons with the same artificial current. It measures
T4 spike counts versus no stimulus. It does **not** test spatial direction
selectivity, and the weights remain excitatory engineering placeholders.
Plasticity is deliberately disabled in the initial real-connectome baseline.
