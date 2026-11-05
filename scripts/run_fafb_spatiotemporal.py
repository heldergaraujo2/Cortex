"""Run paired opposite ON-front stimuli over one FAFB medulla hemisphere."""
from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

from cortex.connectome import load_pilot_connectome
from cortex.dynamics import build_rate_network, run_rate_simulation_schedule
from cortex.spatial import load_column_assignments
from cortex.visual_stimuli import build_lattice_schedule


def _metrics(result: dict[str, object]) -> dict[str, object]:
    return result["metrics"]


def run_experiment(data_dir: Path, neuropil: str, minimum_synapses: int = 5) -> dict[str, object]:
    if neuropil not in {"ME_L", "ME_R"}:
        raise ValueError("neuropil must be ME_L or ME_R")
    hemisphere = "left" if neuropil == "ME_L" else "right"
    graph = load_pilot_connectome(data_dir)
    assignments = load_column_assignments(
        data_dir / "column_assignment.csv.gz", graph.cell_types
    )
    network = build_rate_network(graph, neuropil, minimum_synapses)
    spatial_summary = assignments.summary(graph.cell_types)
    global_l1_coverage = spatial_summary["coverage_by_primary_type"]["L1"]["coverage_fraction"]

    # Restrict the measured T4 population to cells assigned to this hemisphere.
    # The graph contains both hemispheres even when only one neuropil is selected.
    t4_ids_by_subtype = {
        subtype: tuple(sorted({
            row.root_id for row in assignments.rows
            if row.hemisphere == hemisphere
            and row.cell_type == subtype
            and row.root_id in network.neuron_types
        }))
        for subtype in ("T4a", "T4b", "T4c", "T4d")
    }
    side_t4_ids = tuple(sorted(
        root_id for ids in t4_ids_by_subtype.values() for root_id in ids
    ))
    if not side_t4_ids:
        raise ValueError(f"no assigned T4 readout neurons for hemisphere {hemisphere!r}")
    network = replace(
        network,
        readout_ids=side_t4_ids,
        readout_ids_by_subtype=t4_ids_by_subtype,
    )
    schedules = {}

    for axis in ("p", "q", "v"):
        positive = build_lattice_schedule(
            assignments.rows, network.input_ids, hemisphere, axis, 1
        )
        negative = build_lattice_schedule(
            assignments.rows, network.input_ids, hemisphere, axis, -1
        )
        if positive.frames != tuple(reversed(negative.frames)):
            raise AssertionError("opposite directions must be exact frame reversals")
        if positive.total_input_events != negative.total_input_events:
            raise AssertionError("opposite directions must have equal input energy")

        plus_result = run_rate_simulation_schedule(network, positive.frames)
        minus_result = run_rate_simulation_schedule(network, negative.frames)
        plus_activity = _metrics(plus_result)["integrated_t4_activity"]
        minus_activity = _metrics(minus_result)["integrated_t4_activity"]
        denominator = plus_activity + minus_activity
        asymmetry = (
            abs(plus_activity - minus_activity) / denominator
            if denominator > 0 else None
        )

        all_assigned_l1 = positive.active_root_ids
        empty_schedule = tuple(frozenset() for _ in positive.frames)
        static_schedule = (frozenset(all_assigned_l1),) + tuple(
            frozenset() for _ in positive.frames[1:]
        )
        schedules[axis] = {
            "axis_definition": {
                "p": "anterodorsal in medulla lattice; progress=2p-q",
                "q": "posterodorsal in medulla lattice; progress=2q-p",
                "v": "dorsal in medulla lattice; progress=p+q",
            }[axis],
            "input": {
                "assigned_l1_neurons": len(all_assigned_l1),
                "l1_neurons_in_graph_both_hemispheres": len(network.input_ids),
                "global_l1_assignment_coverage_both_hemispheres": global_l1_coverage,
                "hemisphere_specific_l1_coverage": None,
                "frames": len(positive.frames),
                "total_l1_input_events_per_direction": positive.total_input_events,
                "progress_min": min(positive.progress_values),
                "progress_max": max(positive.progress_values),
            },
            "positive_direction": _metrics(plus_result),
            "negative_direction": _metrics(minus_result),
            "lattice_response_asymmetry_index": asymmetry,
            "static_full_field_control": _metrics(
                run_rate_simulation_schedule(network, static_schedule)
            ),
            "no_stimulus_control": _metrics(
                run_rate_simulation_schedule(network, empty_schedule)
            ),
        }

    return {
        "experiment": "fafb-v783-medulla-lattice-moving-front-diagnostic-v1",
        "dataset": "FlyWire FAFB v783",
        "neuropil": neuropil,
        "hemisphere": hemisphere,
        "coordinate_frame": (
            "medulla p/q hexagonal lattice only; not retinal, eye-spherical, "
            "world-space or animal-motion coordinates"
        ),
        "source_files": list(graph.file_manifest) + [{
            "file": "column_assignment.csv.gz",
            "size_bytes": assignments.size_bytes,
            "sha256": assignments.sha256,
        }],
        "network": {
            "neurons": len(network.neuron_types),
            "edges": len(network.edges),
            "l1_input_neurons": len(network.input_ids),
            "t4_readout_assigned_to_hemisphere": len(network.readout_ids),
            "t4_readout_by_subtype": {
                subtype: len(ids) for subtype, ids in network.readout_ids_by_subtype.items()
            },
            "minimum_synapses": minimum_synapses,
        },
        "model_limits": [
            "Structural rate-based diagnostic only; no biological time calibration.",
            "No inhibitory T4 inputs (for example Mi4/Mi9/C3/CT1) in this pilot graph.",
            "No synaptic delays, membrane dynamics, nonlinear dendritic integration or plasticity.",
            "The asymmetry index is not a biological direction-selectivity index.",
            "T4a-T4d are reported separately but no subtype is assigned a preferred direction.",
            "No mapping from medulla lattice motion to retinal/world visual motion is claimed.",
        ],
        "axes": schedules,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw/fafb_v783"))
    parser.add_argument("--neuropil", choices=("ME_L", "ME_R"), required=True)
    parser.add_argument("--minimum-synapses", type=int, default=5)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = run_experiment(args.data_dir, args.neuropil, args.minimum_synapses)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "output": str(args.output),
        "neuropil": report["neuropil"],
        "axes": {
            axis: {
                "steps": data["input"]["frames"],
                "assigned_l1": data["input"]["assigned_l1_neurons"],
                "t4_readout": report["network"]["t4_readout_assigned_to_hemisphere"],
                "asymmetry": data["lattice_response_asymmetry_index"],
                "plus_peak": data["positive_direction"]["peak_mean_t4_rate"],
                "minus_peak": data["negative_direction"]["peak_mean_t4_rate"],
            }
            for axis, data in report["axes"].items()
        },
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
