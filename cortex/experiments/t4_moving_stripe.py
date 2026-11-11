"""Exploratory moving-stripe stimulation of a real FAFB-derived topology.

Stimulus, current, synaptic weights and time scale are synthetic; this is NOT
a validated visual response or proof of biological direction selectivity.
"""
from __future__ import annotations
import argparse
import csv
import gzip
import json
import random
from collections import Counter
from pathlib import Path
from cortex.experiments.t4_selector import select_t4_pilot

SUBTYPES = ("T4a", "T4b", "T4c", "T4d")
DIRECTIONS = (("x+", "x", 1), ("x-", "x", -1), ("y+", "y", 1), ("y-", "y", -1))

def rows(path):
    with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as stream:
        yield from csv.DictReader(stream)

def run(annotations, connections, columns, *, steps=16, current=1.2, shuffle_seed=None):
    if steps < 4 or not 0 < current < 100:
        raise ValueError("invalid stimulus parameters")
    labels = {}
    for row in rows(annotations):
        label = (row.get("primary_type") or "").strip()
        if label in SUBTYPES:
            labels[int(row["root_id"])] = label
    positions = {}
    for row in rows(columns):
        try:
            root = int(row["root_id"])
            x, y = float(row["x"]), float(row["y"])
        except (KeyError, ValueError, TypeError):
            continue
        if root not in positions:
            positions[root] = (x, y)
    selected = select_t4_pilot(annotations, connections, cell_type_column="primary_type")
    roots = selected.circuit.root_ids
    l1 = [(i, positions[root]) for i, root in enumerate(roots)
          if selected.neuron_types[root] == "L1" and root in positions]
    if shuffle_seed is not None:
        shuffled = [position for _, position in l1]
        random.Random(shuffle_seed).shuffle(shuffled)
        l1 = [(index, position) for (index, _), position in zip(l1, shuffled)]
    t4 = {name: [i for i, root in enumerate(roots) if labels.get(root) == name]
          for name in SUBTYPES}
    if not l1 or not all(t4.values()):
        raise ValueError("missing spatially annotated L1 or one or more T4 subtypes")
    circuit = selected.circuit.simulator()
    results = {}
    for name, axis, sign in DIRECTIONS:
        coord = 0 if axis == "x" else 1
        values = [p[coord] for _, p in l1]
        lo, hi = min(values), max(values)
        if hi == lo:
            raise ValueError(f"no {axis} coordinate variation in L1")
        circuit.reset_activity()
        totals = Counter({s: 0 for s in SUBTYPES})
        for step in range(steps):
            fraction = (step + 0.5) / steps
            center = lo + (hi - lo) * (fraction if sign > 0 else 1 - fraction)
            half_width = (hi - lo) / steps
            driven = {i for i, p in l1 if abs(p[coord] - center) <= half_width}
            stimulus = tuple(current if i in driven else 0.0 for i in range(circuit.neuron_count))
            spikes = circuit.step(stimulus, learn=False)
            for subtype, indices in t4.items():
                totals[subtype] += sum(spikes[i] for i in indices)
        results[name] = dict(totals)
    contrasts = {
        axis: {subtype: results[f"{axis}+"][subtype] - results[f"{axis}-"][subtype]
               for subtype in SUBTYPES}
        for axis in ("x", "y")
    }
    return {
        "dataset": "FAFB v783", "connectome_derived": True,
        "spatial_stimulus_implemented": True, "direction_selectivity_validated": False,
        "biologically_validated": False, "plasticity_enabled": False,
        "synthetic_stimulus": "moving coordinate stripe with injected L1 current",
        "synthetic_synaptic_signs": True,
        "steps": steps, "input_current": current,
        "l1_coordinate_shuffle_seed": shuffle_seed,
        "selected_neurons": len(roots), "selected_edges": len(selected.circuit.edges),
        "spatial_l1_neurons": len(l1),
        "t4_subtype_counts": {s: len(t4[s]) for s in SUBTYPES},
        "spikes_by_direction_and_subtype": results,
        "opposing_direction_spike_differences": contrasts,
        "interpretation": "Exploratory response differences are model-dependent, not biological direction selectivity."
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--annotations", required=True)
    p.add_argument("--connections", required=True)
    p.add_argument("--columns", required=True)
    args = p.parse_args()
    print(json.dumps(run(args.annotations, args.connections, args.columns), indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
