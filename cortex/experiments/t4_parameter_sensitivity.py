"""Parameter sensitivity controls for exploratory FAFB T4 moving-stripe experiment.

Uses real connectivity, but artificial stimulation and uncalibrated dynamics.
A sensitivity result is NOT biological validation.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from cortex.experiments.t4_moving_stripe import run

def compare(annotations, connections, columns, *, currents=(0.8, 1.2)):
    experiments = {}
    for current in currents:
        result = run(annotations, connections, columns, current=current)
        experiments[str(current)] = {
            "spikes_by_direction_and_subtype": result["spikes_by_direction_and_subtype"],
            "opposing_direction_spike_differences": result["opposing_direction_spike_differences"],
        }
    signs = {}
    for axis in ("x", "y"):
        signs[axis] = {}
        for subtype in ("T4a", "T4b", "T4c", "T4d"):
            values = [experiments[str(c)]["opposing_direction_spike_differences"][axis][subtype] for c in currents]
            signs[axis][subtype] = {
                "differences": values,
                "nonzero_same_sign": all(v > 0 for v in values) or all(v < 0 for v in values),
            }
    return {
        "dataset": "FAFB v783",
        "connectome_derived": True,
        "control": "input_current_parameter_sensitivity",
        "currents": list(currents),
        "experiments": experiments,
        "directional_contrast_sign_consistency": signs,
        "biologically_validated": False,
        "direction_selectivity_validated": False,
        "limitations": "No randomized spatial control, calibration, uncertainty intervals, or physiological validation."
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--annotations", required=True)
    parser.add_argument("--connections", required=True)
    parser.add_argument("--columns", required=True)
    args = parser.parse_args()
    print(json.dumps(compare(Path(args.annotations), Path(args.connections), Path(args.columns)), indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
