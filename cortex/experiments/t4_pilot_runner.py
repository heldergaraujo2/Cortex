"""Execute a topology-only FAFB T4 pilot from supplied data files.

No spatial motion-selectivity claim: stimulation here is an artificial current
injection into all selected L1 neurons, not a calibrated retinal stimulus.
"""
from __future__ import annotations

import argparse
import json
import hashlib
from pathlib import Path

from cortex.experiments.t4_selector import select_t4_pilot


def run_pilot(cell_types: str | Path, connections: str | Path, *,
              steps: int = 12, input_current: float = 1.2,
              min_synapses: int = 5,
              cell_type_column: str = "cell_type",
              synapse_column: str = "syn_count",
              cell_id_column: str = "root_id",
              pre_column: str = "pre_root_id",
              post_column: str = "post_root_id") -> dict[str, object]:
    if steps < 2 or not 0 < input_current < 100:
        raise ValueError("invalid stimulation")
    selected = select_t4_pilot(
        cell_types, connections, min_synapses=min_synapses,
        cell_type_column=cell_type_column, synapse_column=synapse_column,
        cell_id_column=cell_id_column, pre_column=pre_column,
        post_column=post_column
    )
    circuit = selected.circuit.simulator()
    l1 = [i for i, root in enumerate(selected.circuit.root_ids)
          if selected.neuron_types[root] == "L1"]
    t4 = [i for i, root in enumerate(selected.circuit.root_ids)
          if selected.neuron_types[root] == "T4"]
    if not l1 or not t4:
        from collections import Counter
        counts = dict(Counter(selected.neuron_types.values()))
        raise ValueError(f"pilot must contain L1 and T4 neurons; selected_type_counts={counts}; selected_edge_counts={selected.edge_counts}; likely missing T4 annotations or thresholded T4 input edges")
    def simulate(stimulated: bool) -> int:
        circuit.reset_activity()
        total = 0
        for step in range(steps):
            current = tuple(
                input_current if stimulated and step < steps // 2 and i in l1 else 0.0
                for i in range(circuit.neuron_count)
            )
            spikes = circuit.step(current, learn=False)
            total += sum(spikes[i] for i in t4)
        return total
    baseline = simulate(False)
    driven = simulate(True)
    def fingerprint(path):
        path = Path(path)
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return {"path": str(path), "bytes": path.stat().st_size, "sha256": digest.hexdigest()}
    return {
        "selected_root_ids": list(selected.circuit.root_ids),
        "selected_connections": [list(edge) for edge in selected.circuit.edges],
        "input_files": {"annotations": fingerprint(cell_types), "connections": fingerprint(connections)},
        "dataset": "user_supplied_fafb_format",
        "connectome_derived": True,
        "biologically_validated": False,
        "spatial_motion_test": False,
        "plasticity_enabled": False,
        "selected_neurons": len(selected.circuit.root_ids),
        "selected_edges": len(selected.circuit.edges),
        "edge_counts": selected.edge_counts,
        "t4_spikes_no_stimulus": baseline,
        "t4_spikes_l1_current": driven,
        "source_connections": str(connections),
        "source_annotations": str(cell_types),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cell-types", required=True)
    parser.add_argument("--connections", required=True)
    parser.add_argument("--cell-type-column", default="cell_type")
    parser.add_argument("--synapse-column", default="syn_count")
    parser.add_argument("--cell-id-column", default="root_id")
    parser.add_argument("--pre-column", default="pre_root_id")
    parser.add_argument("--post-column", default="post_root_id")
    parser.add_argument("--steps", type=int, default=12)
    args = parser.parse_args()
    result = run_pilot(
        args.cell_types, args.connections, steps=args.steps,
        cell_type_column=args.cell_type_column, synapse_column=args.synapse_column,
        cell_id_column=args.cell_id_column, pre_column=args.pre_column,
        post_column=args.post_column
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
