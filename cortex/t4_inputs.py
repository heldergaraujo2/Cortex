"""Preserve real FAFB v783 presynaptic candidate edges into T4.

This importer records structure and supplied labels only. It does not infer
synaptic sign, efficacy, delay, or direction preference.
"""
from __future__ import annotations

import csv
import gzip
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

CELL_TYPES_FILE = "consolidated_cell_types.csv.gz"
CONNECTIONS_FILE = "connections_princeton.csv.gz"
T4_INPUT_TYPES = frozenset({"Mi1", "Tm3", "Mi4", "Mi9", "C3", "TmY15", "CT1"})
T4_TYPES = frozenset({"T4a", "T4b", "T4c", "T4d"})


@dataclass(frozen=True, slots=True)
class T4InputEdge:
    pre_root_id: str
    post_root_id: str
    pre_type: str
    post_type: str
    neuropil: str
    syn_count: int
    nt_type: str


def _load_primary_types(path: Path) -> dict[str, str]:
    cell_types: dict[str, str] = {}
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
            if root_id in cell_types:
                raise ValueError(f"{path.name}:{line_number}: duplicate root_id {root_id}")
            if cell_type:
                cell_types[root_id] = cell_type
    return cell_types


def load_t4_input_edges(
    data_dir: str | Path,
    neuropil: str | None = None,
    minimum_synapses: int = 0,
) -> tuple[T4InputEdge, ...]:
    """Load candidate presynaptic rows into T4 without merging or signing them."""
    if neuropil is not None and not neuropil.strip():
        raise ValueError("neuropil must be None or a non-empty exact label")
    if not isinstance(minimum_synapses, int) or minimum_synapses < 0:
        raise ValueError("minimum_synapses must be an integer >= 0")

    root = Path(data_dir)
    cell_types = _load_primary_types(root / CELL_TYPES_FILE)
    path = root / CONNECTIONS_FILE
    edges: list[T4InputEdge] = []
    with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"pre_root_id", "post_root_id", "neuropil", "syn_count", "nt_type"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"{path.name}: expected columns {sorted(required)}")
        for line_number, row in enumerate(reader, start=2):
            pre_id = (row.get("pre_root_id") or "").strip()
            post_id = (row.get("post_root_id") or "").strip()
            pre_type = cell_types.get(pre_id)
            post_type = cell_types.get(post_id)
            if pre_type not in T4_INPUT_TYPES or post_type not in T4_TYPES:
                continue
            edge_neuropil = (row.get("neuropil") or "").strip() or "(empty)"
            if neuropil is not None and edge_neuropil != neuropil:
                continue
            try:
                syn_count = int(row["syn_count"])
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"{path.name}:{line_number}: invalid syn_count {row.get('syn_count')!r}"
                ) from exc
            if syn_count < 0:
                raise ValueError(f"{path.name}:{line_number}: negative syn_count")
            if syn_count < minimum_synapses:
                continue
            edges.append(T4InputEdge(
                pre_root_id=pre_id,
                post_root_id=post_id,
                pre_type=pre_type,
                post_type=post_type,
                neuropil=edge_neuropil,
                syn_count=syn_count,
                nt_type=(row.get("nt_type") or "").strip() or "(empty)",
            ))
    return tuple(edges)


def summarize_t4_input_edges(edges: tuple[T4InputEdge, ...]) -> dict[str, object]:
    rows: Counter[tuple[str, str, str, str]] = Counter()
    synapses: Counter[tuple[str, str, str, str]] = Counter()
    unique_pairs: dict[tuple[str, str, str], set[tuple[str, str]]] = {}
    for edge in edges:
        key = (edge.pre_type, edge.post_type, edge.neuropil, edge.nt_type)
        rows[key] += 1
        synapses[key] += edge.syn_count
        unique_pairs.setdefault((edge.pre_type, edge.post_type, edge.neuropil), set()).add(
            (edge.pre_root_id, edge.post_root_id)
        )
    grouped = [
        {
            "pre_type": pre,
            "post_type": post,
            "neuropil": region,
            "nt_type_as_supplied": nt,
            "table_rows": rows[(pre, post, region, nt)],
            "distinct_pre_post_pairs_within_group": len(unique_pairs[(pre, post, region)]),
            "syn_count_sum": synapses[(pre, post, region, nt)],
        }
        for pre, post, region, nt in sorted(rows)
    ]
    return {
        "dataset": "FlyWire FAFB v783",
        "candidate_input_rows": len(edges),
        "unique_presynaptic_root_ids": len({edge.pre_root_id for edge in edges}),
        "unique_postsynaptic_t4_root_ids": len({edge.post_root_id for edge in edges}),
        "rows_by_type_neuropil_nt_type": grouped,
        "synaptic_sign_assigned": False,
        "aggregation_note": (
            "Rows are preserved as supplied. syn_count is structural; nt_type is an annotation "
            "label, not a verified per-edge physiological sign. No efficacy or delay is inferred."
        ),
    }
