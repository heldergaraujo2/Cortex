"""FAFB-compatible edge adapter for the experimental LIF simulator.

Accepts an explicitly supplied connections CSV/CSV.GZ with pre_root_id,
post_root_id, and syn_count. No invented root IDs or synaptic signs.
This is a *structural* import, not validated fly-brain dynamics.
"""
from __future__ import annotations

import csv
import gzip
from dataclasses import dataclass
from pathlib import Path

from cortex.experiments.spiking_circuit import SpikingCircuit, Synapse


@dataclass(frozen=True)
class ImportedCircuit:
    root_ids: tuple[int, ...]
    edges: tuple[tuple[int, int, int], ...]
    source: str

    def simulator(self, *, weight_scale: float = 0.05) -> SpikingCircuit:
        if not 0 < weight_scale <= 1:
            raise ValueError("weight_scale must be in (0, 1]")
        indices = {root: index for index, root in enumerate(self.root_ids)}
        # This simulator only models nonnegative synapses. These weights
        # are placeholders; neurotransmitter polarity is NOT inferred.
        synapses = [
            Synapse(indices[pre], indices[post], min(2.0, count * weight_scale))
            for pre, post, count in self.edges
        ]
        return SpikingCircuit(len(self.root_ids), synapses)


def import_connections(
    path: str | Path, selected_root_ids: set[int], *,
    min_synapses: int = 1, max_edges: int = 100000,
    pre_column: str = "pre_root_id", post_column: str = "post_root_id",
    count_column: str = "syn_count",
) -> ImportedCircuit:
    """Stream selected induced subgraph from a real connections table.

    The caller must supply verified FAFB root IDs; this function does not
    invent a biological circuit or claim the selected nodes are T4 neurons.
    """
    path = Path(path)
    if not selected_root_ids or any(type(x) is not int or x <= 0 for x in selected_root_ids):
        raise ValueError("selected_root_ids must contain positive integer root IDs")
    if min_synapses < 1 or max_edges < 1:
        raise ValueError("invalid import limits")
    if not path.is_file():
        raise FileNotFoundError(path)
    opener = gzip.open if path.suffix.lower() == ".gz" else open
    edges: list[tuple[int, int, int]] = []
    with opener(path, "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {pre_column, post_column, count_column}
        if not required.issubset(reader.fieldnames or ()):
            raise ValueError(f"missing columns: {sorted(required - set(reader.fieldnames or ())) }")
        for row in reader:
            try:
                pre = int(row[pre_column])
                post = int(row[post_column])
            except (ValueError, TypeError) as exc:
                raise ValueError("invalid root ID in connection data") from exc
            if pre not in selected_root_ids or post not in selected_root_ids:
                continue
            try:
                count = int(row[count_column])
            except (ValueError, TypeError) as exc:
                raise ValueError("invalid synapse count") from exc
            if count < 0:
                raise ValueError("negative synapse count")
            if count >= min_synapses:
                edges.append((pre, post, count))
                if len(edges) > max_edges:
                    raise ValueError("selected subgraph exceeds max_edges")
    if not edges:
        raise ValueError("no matching connections for selected IDs")
    roots = tuple(sorted({x for pre, post, _ in edges for x in (pre, post)}))
    return ImportedCircuit(roots, tuple(edges), str(path))
