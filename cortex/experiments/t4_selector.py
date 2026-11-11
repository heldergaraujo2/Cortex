"""Reproducible selection of an annotated FAFB ON-motion pilot subgraph.

The caller supplies downloaded official CSV files. Column names are explicit,
because FlyWire products and versions can differ. No IDs are invented.
"""
from __future__ import annotations

import csv
import gzip
from dataclasses import dataclass
from pathlib import Path

from cortex.experiments.connectome_adapter import ImportedCircuit

CELL_TYPES = frozenset({"L1", "Mi1", "Tm3", "T4"})
T4_SUBTYPES = frozenset({"T4a", "T4b", "T4c", "T4d"})


def _pilot_type(annotation: str) -> str:
    """Normalize established T4 directional subtypes without inventing neuron IDs."""
    value = annotation.strip()
    return "T4" if value in T4_SUBTYPES else value

ALLOWED_PAIRS = frozenset({
    ("L1", "Mi1"), ("L1", "Tm3"), ("Mi1", "T4"), ("Tm3", "T4")
})


def _rows(path: str | Path):
    path = Path(path)
    opener = gzip.open if path.suffix.lower() == ".gz" else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as stream:
        yield from csv.DictReader(stream)


@dataclass(frozen=True)
class T4Selection:
    circuit: ImportedCircuit
    neuron_types: dict[int, str]
    edge_counts: dict[str, int]


def select_t4_pilot(
    cell_types_path: str | Path,
    connections_path: str | Path,
    *,
    cell_id_column: str = "root_id",
    cell_type_column: str = "cell_type",
    pre_column: str = "pre_root_id",
    post_column: str = "post_root_id",
    synapse_column: str = "syn_count",
    min_synapses: int = 5,
    max_selected_neurons: int = 50000,
    max_selected_edges: int = 200000,
) -> T4Selection:
    if min_synapses < 1 or max_selected_neurons < 1 or max_selected_edges < 1:
        raise ValueError("invalid selection limits")
    types: dict[int, str] = {}
    saw_cells = False
    for row in _rows(cell_types_path):
        if not saw_cells:
            if not {cell_id_column, cell_type_column}.issubset(row):
                raise ValueError("cell type CSV missing required columns")
            saw_cells = True
        cell_type = _pilot_type(row[cell_type_column] or "")
        if cell_type in CELL_TYPES:
            root = int(row[cell_id_column])
            if root <= 0:
                raise ValueError("invalid root ID")
            if root in types and types[root] != cell_type:
                raise ValueError("conflicting cell type annotations")
            types[root] = cell_type
            if len(types) > max_selected_neurons:
                raise ValueError("selected neurons exceed limit")
    if not types:
        raise ValueError("no annotated L1/Mi1/Tm3/T4 neurons found")
    edges: list[tuple[int, int, int]] = []
    counts: dict[str, int] = {}
    saw_connections = False
    for row in _rows(connections_path):
        if not saw_connections:
            if not {pre_column, post_column, synapse_column}.issubset(row):
                raise ValueError("connections CSV missing required columns")
            saw_connections = True
        pre, post = int(row[pre_column]), int(row[post_column])
        if pre not in types or post not in types:
            continue
        pair = (types[pre], types[post])
        if pair not in ALLOWED_PAIRS:
            continue
        count = int(row[synapse_column])
        if count < 0:
            raise ValueError("negative synapse count")
        if count < min_synapses:
            continue
        edges.append((pre, post, count))
        key = f"{pair[0]}->{pair[1]}"
        counts[key] = counts.get(key, 0) + 1
        if len(edges) > max_selected_edges:
            raise ValueError("selected edges exceed limit")
    if not edges:
        raise ValueError("no qualifying T4 pilot connections")
    selected = {root for pre, post, _ in edges for root in (pre, post)}
    return T4Selection(
        ImportedCircuit(tuple(sorted(selected)), tuple(edges), str(connections_path)),
        {root: types[root] for root in sorted(selected)},
        counts,
    )
