"""Audit annotated presynaptic candidates and transmitter labels for T4.

This is an evidence inventory, not a signed synapse model. The connection
product's nt_type is reported as supplied and is never converted into an
excitatory/inhibitory sign here.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
from collections import Counter
from pathlib import Path

CELL_FILE = "consolidated_cell_types.csv.gz"
CONNECTION_FILE = "connections_princeton.csv.gz"
T4_INPUT_CANDIDATES = ("Mi1", "Tm3", "Mi4", "Mi9", "C3", "TmY15", "CT1")


def load_primary_types(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"root_id", "primary_type"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"{path.name}: expected columns {sorted(required)}")
        for line_number, row in enumerate(reader, start=2):
            root_id = (row.get("root_id") or "").strip()
            cell_type = (row.get("primary_type") or "").strip()
            if not root_id:
                raise ValueError(f"{path.name}:{line_number}: empty root_id")
            if root_id in result:
                raise ValueError(f"{path.name}:{line_number}: duplicate root_id {root_id}")
            if cell_type:
                result[root_id] = cell_type
    return result


def audit_t4_inputs(data_dir: Path) -> dict[str, object]:
    cell_types = load_primary_types(data_dir / CELL_FILE)
    counts = Counter(cell_types.values())
    candidate_counts = {
        cell_type: counts[cell_type] for cell_type in T4_INPUT_CANDIDATES
    }
    candidate_counts["T4a"] = counts["T4a"]
    candidate_counts["T4b"] = counts["T4b"]
    candidate_counts["T4c"] = counts["T4c"]
    candidate_counts["T4d"] = counts["T4d"]

    rows_total = 0
    mapped_both = 0
    pair_rows: Counter[tuple[str, str, str, str]] = Counter()
    pair_synapses: Counter[tuple[str, str, str, str]] = Counter()
    transmitter_rows: Counter[str] = Counter()
    unmapped_candidate_endpoint_rows = 0
    candidate_set = set(T4_INPUT_CANDIDATES)

    connection_path = data_dir / CONNECTION_FILE
    with gzip.open(connection_path, "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"pre_root_id", "post_root_id", "neuropil", "syn_count", "nt_type"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"{connection_path.name}: expected columns {sorted(required)}")
        for line_number, row in enumerate(reader, start=2):
            rows_total += 1
            pre_id = (row.get("pre_root_id") or "").strip()
            post_id = (row.get("post_root_id") or "").strip()
            pre_type = cell_types.get(pre_id)
            post_type = cell_types.get(post_id)
            if pre_type in candidate_set and post_type is None:
                unmapped_candidate_endpoint_rows += 1
            if not pre_type or not post_type:
                continue
            mapped_both += 1
            if pre_type not in candidate_set or not post_type.startswith("T4"):
                continue
            try:
                syn_count = int(row["syn_count"])
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"{connection_path.name}:{line_number}: invalid syn_count "
                    f"{row.get('syn_count')!r}"
                ) from exc
            if syn_count < 0:
                raise ValueError(
                    f"{connection_path.name}:{line_number}: negative syn_count"
                )
            neuropil = (row.get("neuropil") or "").strip() or "(empty)"
            nt_type = (row.get("nt_type") or "").strip() or "(empty)"
            key = (pre_type, post_type, neuropil, nt_type)
            pair_rows[key] += 1
            pair_synapses[key] += syn_count
            transmitter_rows[nt_type] += 1

    pairs = [
        {
            "presynaptic_primary_type": pre,
            "postsynaptic_primary_type": post,
            "neuropil": neuropil,
            "nt_type_as_supplied": nt_type,
            "table_rows": pair_rows[(pre, post, neuropil, nt_type)],
            "syn_count_sum_within_neuropil_and_nt_type": pair_synapses[(pre, post, neuropil, nt_type)],
        }
        for pre, post, neuropil, nt_type in sorted(pair_rows)
    ]
    return {
        "dataset": "FlyWire FAFB v783",
        "purpose": "Evidence inventory of annotated candidate inputs to T4",
        "primary_type_source": CELL_FILE,
        "connection_source": CONNECTION_FILE,
        "candidate_presynaptic_types": list(T4_INPUT_CANDIDATES),
        "candidate_and_T4_primary_type_counts": candidate_counts,
        "connection_rows_total": rows_total,
        "connection_rows_with_both_ids_mapped": mapped_both,
        "candidate_pre_to_T4_connection_rows": sum(pair_rows.values()),
        "candidate_pre_to_T4_pairs_by_type_neuropil_and_nt": pairs,
        "nt_type_row_counts_as_supplied": dict(sorted(transmitter_rows.items())),
        "unmapped_candidate_pre_endpoint_rows": unmapped_candidate_endpoint_rows,
        "interpretation_limits": [
            "primary_type counts are annotations in the selected table, not proof of complete cell-class coverage",
            "nt_type is reported verbatim and is not treated as a definitive per-neuron transmitter sign",
            "syn_count is a structural count, not a calibrated synaptic efficacy",
            "rows remain separated by neuropil and nt_type",
            "anatomical presence does not establish functional inhibition, delay, or direction selectivity",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw/fafb_v783"))
    parser.add_argument("--output", type=Path, default=Path("fafb_v783_t4_input_audit.json"))
    args = parser.parse_args()
    report = audit_t4_inputs(args.data_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"REPORT_PATH: {args.output.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
