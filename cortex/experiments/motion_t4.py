"""Metadata-only specification for the first FAFB visual-circuit pilot.

This module deliberately contains no fabricated root IDs or downloaded data.
"""
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DirectedCellTypeEdge:
    pre_type: str
    post_type: str


@dataclass(frozen=True, slots=True)
class CircuitSpec:
    dataset: str
    snapshot: str
    circuit_id: str
    cell_types: tuple[str, ...]
    edges: tuple[DirectedCellTypeEdge, ...]
    minimum_synapses_per_pair: int
    preserve_neuropil_rows: bool = True


FAFB_V783_T4_ON_CORE = CircuitSpec(
    dataset="FlyWire FAFB",
    snapshot="v783",
    circuit_id="fafb-v783-t4-on-motion-core-v0",
    cell_types=("L1", "Mi1", "Tm3", "T4"),
    edges=(
        DirectedCellTypeEdge("L1", "Mi1"),
        DirectedCellTypeEdge("L1", "Tm3"),
        DirectedCellTypeEdge("Mi1", "T4"),
        DirectedCellTypeEdge("Tm3", "T4"),
    ),
    minimum_synapses_per_pair=5,
)


def validate_circuit_spec(spec: CircuitSpec) -> None:
    """Reject underspecified metadata before any future importer runs."""
    if not spec.dataset.strip() or not spec.snapshot.strip() or not spec.circuit_id.strip():
        raise ValueError("dataset, snapshot and circuit_id must be non-empty")
    if not spec.cell_types or any(not item.strip() for item in spec.cell_types):
        raise ValueError("cell_types must contain non-empty labels")
    if len(set(spec.cell_types)) != len(spec.cell_types):
        raise ValueError("cell_types must be unique")
    if not spec.edges:
        raise ValueError("at least one directed edge is required")
    allowed = set(spec.cell_types)
    for edge in spec.edges:
        if edge.pre_type not in allowed or edge.post_type not in allowed:
            raise ValueError("edge endpoints must be declared cell types")
    if spec.minimum_synapses_per_pair < 1:
        raise ValueError("minimum_synapses_per_pair must be positive")
