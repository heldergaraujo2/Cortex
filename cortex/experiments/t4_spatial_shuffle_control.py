"""Negative control: permute L1 spatial positions while preserving FAFB edges."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from cortex.experiments.t4_moving_stripe import run, SUBTYPES

def control(annotations, connections, columns, seeds=(11, 29, 47)):
    original = run(annotations, connections, columns)
    shuffled = [run(annotations, connections, columns, shuffle_seed=seed) for seed in seeds]
    contrasts = lambda result: result["opposing_direction_spike_differences"]
    summary = {}
    for axis in ("x", "y"):
        summary[axis] = {}
        for subtype in SUBTYPES:
            observed = contrasts(original)[axis][subtype]
            null = [contrasts(item)[axis][subtype] for item in shuffled]
            summary[axis][subtype] = {
                "observed_difference": observed,
                "shuffled_differences": null,
                "observed_exceeds_all_shuffled_absolute_differences": all(abs(observed) > abs(x) for x in null),
            }
    return {
        "connectome_derived": True,
        "control": "seeded_L1_coordinate_permutation",
        "preserved": ["neuron identities", "synaptic edges", "synapse counts", "L1 coordinate distribution"],
        "shuffled_seeds": list(seeds),
        "directional_contrasts": summary,
        "biologically_validated": False,
        "direction_selectivity_validated": False,
        "note": "Three permutations are a technical negative control, not a statistically powered significance test."
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--annotations", required=True)
    p.add_argument("--connections", required=True)
    p.add_argument("--columns", required=True)
    args = p.parse_args()
    print(json.dumps(control(Path(args.annotations), Path(args.connections), Path(args.columns)), indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
