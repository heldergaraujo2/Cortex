"""FAFB v783 exploratory T4 graph experiment; not biological validation."""
import argparse
import csv
import gzip
import json
from collections import Counter
from pathlib import Path

from cortex.experiments.t4_spatial_stimuli import generate, read_rows
from cortex.experiments.t4_directional_response import simulate, direction_metrics, T4_TYPES


def graph_inputs(annotations, connections, allowed_roots):
    types = {}
    for row in read_rows(annotations):
        if row.get("primary_type") in T4_TYPES:
            types[row["root_id"]] = row["primary_type"]
    allowed = set(map(str, allowed_roots))
    allowed.update(types)
    edges = []
    with gzip.open(connections, "rt", encoding="utf-8-sig", newline="") if str(connections).endswith(".gz") else open(connections, "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fields = set(reader.fieldnames or ())
        def column(*names):
            return next((name for name in names if name in fields), None)
        pre = column("pre_root_id", "pre_pt_root_id", "pre_id")
        post = column("post_root_id", "post_pt_root_id", "post_id")
        weight = column("syn_count", "synapse_count", "weight", "count", "n_synapses")
        if not all((pre, post, weight)):
            raise ValueError("Unsupported connectivity columns: " + str(sorted(fields)))
        # Keep only a bounded two-hop feed-forward neighborhood of stimulated L1.
        rows = []
        first_hop = set()
        for row in reader:
            a, b = row[pre], row[post]
            if a in allowed_roots:
                first_hop.add(b)
            rows.append((a, b, row[weight]))
        retained = set(map(str, allowed_roots)) | first_hop | set(types)
        for a, b, w in rows:
            if a in retained and b in retained:
                try:
                    n = float(w)
                    if 0 < n < float("inf"):
                        edges.append((a, b, n))
                except (ValueError, TypeError):
                    continue
    return types, edges


def experiment(annotations, columns, connections, steps=12):
    inputs = generate(annotations, columns, steps=steps)
    schedules = inputs["directions"]
    roots = {str(root) for frames in schedules.values() for frame in frames
             for root in frame["active_l1_root_ids"]}
    types, edges = graph_inputs(annotations, connections, roots)
    response = simulate(schedules, edges, types, normalize_outgoing=True)
    return {"schema": "cortex.t4_real_graph_experiment.v1",
            "input_schema": inputs["schema"],
            "mapped_l1_neurons": inputs["mapped_l1_neurons"],
            "stimulated_l1_neurons": len(roots),
            "retained_edges": len(edges),
            "t4_annotation_counts": dict(Counter(types.values())),
            "metrics": direction_metrics(response),
            "responses": response,
            "real_fafb_experiment_executed": True,
            "biological_direction_selectivity_validated": False,
            "limitations": ["Simplified nonnegative weighted propagation with outgoing normalization",
                            "No inhibitory sign or cell physiology calibration",
                            "Column axes are not calibrated visual angles",
                            "Direction contrasts require matched controls and replication"]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--annotations", type=Path, required=True)
    p.add_argument("--columns", type=Path, required=True)
    p.add_argument("--connections", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    result = experiment(args.annotations, args.columns, args.connections)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(args.output), "edges": result["retained_edges"],
                      "t4_counts": result["t4_annotation_counts"]}))


if __name__ == "__main__":
    main()
