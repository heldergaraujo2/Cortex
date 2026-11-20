"""Exploratory permutation test of FAFB T4 moving-stripe contrasts.

Preserves the real connectivity and L1 coordinate distribution; randomly
reassigns coordinates to L1 identities. This is not biological validation.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from cortex.experiments.t4_moving_stripe import run, SUBTYPES

def analyze(annotations, connections, columns, *, permutations=19, seed_start=1000):
    if permutations < 1:
        raise ValueError("permutations must be positive")
    original = run(annotations, connections, columns)
    null = [
        run(annotations, connections, columns, shuffle_seed=seed_start + i)
        for i in range(permutations)
    ]
    comparisons = {}
    for axis in ("x", "y"):
        comparisons[axis] = {}
        for subtype in SUBTYPES:
            observed = original["opposing_direction_spike_differences"][axis][subtype]
            samples = [result["opposing_direction_spike_differences"][axis][subtype] for result in null]
            exceedances = sum(abs(sample) >= abs(observed) for sample in samples)
            comparisons[axis][subtype] = {
                "observed_signed_contrast": observed,
                "null_signed_contrasts": samples,
                "null_mean_signed_contrast": sum(samples) / len(samples),
                "null_min_signed_contrast": min(samples),
                "null_max_signed_contrast": max(samples),
                "two_sided_absolute_permutation_p": (1 + exceedances) / (permutations + 1),
                "permutations_at_least_as_extreme": exceedances,
            }
    return {
        "dataset": "FAFB v783",
        "control": "permutation_of_L1_coordinates_with_fixed_connectome",
        "number_of_permutations": permutations,
        "seed_start": seed_start,
        "p_value_method": "plus-one Monte Carlo permutation, two-sided absolute contrast",
        "minimum_attainable_p": 1 / (permutations + 1),
        "multiple_comparisons": 8,
        "comparisons": comparisons,
        "biologically_validated": False,
        "direction_selectivity_validated": False,
        "limitations": "Exploratory; no familywise multiplicity adjustment, coordinate/hemisphere stratification, or physiology calibration. Null may be inappropriate if spatial structure is heterogeneous."
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--annotations", required=True)
    p.add_argument("--connections", required=True)
    p.add_argument("--columns", required=True)
    p.add_argument("--permutations", type=int, default=19)
    args = p.parse_args()
    print(json.dumps(analyze(Path(args.annotations), Path(args.connections), Path(args.columns), permutations=args.permutations), indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
