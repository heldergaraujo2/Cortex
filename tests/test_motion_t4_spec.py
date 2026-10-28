import pytest

from cortex.experiments.motion_t4 import (
    FAFB_V783_T4_ON_CORE,
    CircuitSpec,
    DirectedCellTypeEdge,
    validate_circuit_spec,
)


def test_initial_circuit_spec_is_explicit_and_reproducible():
    spec = FAFB_V783_T4_ON_CORE
    validate_circuit_spec(spec)
    assert spec.dataset == "FlyWire FAFB"
    assert spec.snapshot == "v783"
    assert spec.cell_types == ("L1", "Mi1", "Tm3", "T4")
    assert spec.minimum_synapses_per_pair == 5
    assert {(edge.pre_type, edge.post_type) for edge in spec.edges} == {
        ("L1", "Mi1"),
        ("L1", "Tm3"),
        ("Mi1", "T4"),
        ("Tm3", "T4"),
    }


def test_circuit_spec_rejects_undeclared_edge_type():
    invalid = CircuitSpec(
        dataset="FAFB",
        snapshot="v783",
        circuit_id="bad",
        cell_types=("L1", "T4"),
        edges=(DirectedCellTypeEdge("L1", "Mi1"),),
        minimum_synapses_per_pair=5,
    )
    with pytest.raises(ValueError):
        validate_circuit_spec(invalid)


def test_circuit_spec_rejects_invalid_threshold():
    invalid = CircuitSpec(
        dataset="FAFB",
        snapshot="v783",
        circuit_id="bad",
        cell_types=("L1", "T4"),
        edges=(DirectedCellTypeEdge("L1", "T4"),),
        minimum_synapses_per_pair=0,
    )
    with pytest.raises(ValueError):
        validate_circuit_spec(invalid)
