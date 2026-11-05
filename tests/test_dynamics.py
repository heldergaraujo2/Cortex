import pytest

from cortex.connectome import PilotConnectome, PilotConnection
from cortex.dynamics import (
    RateConfig, RateEdge, RateNetwork, build_rate_network,
    run_baseline_experiment, run_rate_simulation,
)


def _network():
    return RateNetwork(
        "ME_L",
        {"l1": "L1", "m1": "Mi1", "tm": "Tm3", "t4": "T4a"},
        (
            RateEdge("l1", "m1", 1.0, 10, "L1", "Mi1"),
            RateEdge("l1", "tm", 1.0, 10, "L1", "Tm3"),
            RateEdge("m1", "t4", 0.5, 5, "Mi1", "T4a"),
            RateEdge("tm", "t4", 0.5, 5, "Tm3", "T4a"),
        ),
        ("l1",), ("t4",), {"T4a": ("t4",), "T4b": (), "T4c": (), "T4d": ()},
    )


def _connectome():
    edges = (
        PilotConnection("l1", "m1", "L1", "Mi1", "ME_L", 10, "ACH"),
        PilotConnection("l1", "tm", "L1", "Tm3", "ME_L", 10, "ACH"),
        PilotConnection("m1", "t4", "Mi1", "T4a", "ME_L", 10, "ACH"),
        PilotConnection("tm", "t4", "Tm3", "T4a", "ME_L", 10, "ACH"),
    )
    return PilotConnectome(
        "test", {"l1": "L1", "m1": "Mi1", "tm": "Tm3", "t4": "T4a"},
        {}, edges, (), 4, 0, 0, 4, 4, 4, 0,
    )


def test_pulse_propagates_through_two_stages_deterministically():
    config = RateConfig(steps=6, stimulus_duration=1, leak=1.0)
    first = run_rate_simulation(_network(), config)
    assert first == run_rate_simulation(_network(), config)
    assert first["metrics"]["t4_rate_trace"] == [0.0, 0.0, 1.0, 0.0, 0.0, 0.0]


def test_no_stimulus_control_stays_at_zero():
    result = run_rate_simulation(_network(), RateConfig(steps=5), stimulus=False)
    assert result["metrics"]["peak_mean_t4_rate"] == 0.0


def test_rate_state_is_bounded_and_nonnegative():
    trace = run_rate_simulation(_network(), RateConfig(steps=10))["metrics"]["t4_rate_trace"]
    assert all(0.0 <= value <= 1.0 for value in trace)


@pytest.mark.parametrize("kwargs", [
    {"steps": 0}, {"stimulus_start": -1},
    {"stimulus_start": 3, "stimulus_duration": 2, "steps": 4},
    {"amplitude": 1.1}, {"leak": 0.0}, {"minimum_synapses": 0},
])
def test_invalid_config_is_rejected(kwargs):
    with pytest.raises(ValueError):
        RateConfig(**kwargs).validate()


def test_network_uses_one_neuropil_and_only_declared_edges():
    c = _connectome()
    mixed = PilotConnectome(
        c.dataset, c.cell_types, c.coordinates_by_root_id,
        c.connections + (
            PilotConnection("l1", "t4", "L1", "T4a", "ME_L", 12, "ACH"),
            PilotConnection("l1", "tm", "L1", "Tm3", "ME_R", 12, "ACH"),
            PilotConnection("tm", "t4", "Tm3", "T4a", "ME_L", 4, "ACH"),
        ),
        c.file_manifest, 7, 0, 0, 7, 7, 7, 0,
    )
    network = build_rate_network(mixed, "ME_L", minimum_synapses=5)
    assert {(e.pre_root_id, e.post_root_id) for e in network.edges} == {
        ("l1", "m1"), ("l1", "tm"), ("m1", "t4"), ("tm", "t4")
    }
    assert sum(e.weight for e in network.edges if e.post_root_id == "t4") == pytest.approx(1.0)


def test_ablation_removes_selected_pathway():
    network = build_rate_network(_connectome(), "ME_L", ablate_type="Mi1")
    assert "m1" not in network.neuron_types
    assert all(e.pre_type != "Mi1" and e.post_type != "Mi1" for e in network.edges)


def test_experiment_includes_controls_and_ablations():
    report = run_baseline_experiment(_connectome(), "ME_L", RateConfig(steps=6))
    assert set(report["scenarios"]) == {
        "pulse", "no_stimulus", "pulse_without_Mi1", "pulse_without_Tm3"
    }
    assert report["comparison"]["direction_selectivity_claimed"] is False
