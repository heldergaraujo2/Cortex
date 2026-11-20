"""Deterministic targeted tests for synthetic LIF/STDP circuit."""
import pytest

from cortex.experiments.spiking_circuit import Synapse, SpikingCircuit, timing_experiment


def test_spike_threshold_and_reset():
    net = SpikingCircuit(1, [], leak=0.5)
    assert net.step((0.6,)) == (False,)
    assert net.step((0.8,)) == (True,)
    assert net.voltage == [0.0]


def test_synapse_has_one_step_delay():
    net = SpikingCircuit(2, [Synapse(0, 1, 1.2)], leak=0.0)
    assert net.step((1.1, 0.0)) == (True, False)
    assert net.step((0.0, 0.0)) == (False, True)


def test_causal_timing_potentiates():
    result = timing_experiment()
    assert result["causal_weight"] > result["initial_weight"]
    assert result["anticausal_weight"] < result["initial_weight"]
    assert result["connectome_derived"] is False


def test_learning_can_be_disabled():
    net = SpikingCircuit(2, [Synapse(0, 1, 0.5)], leak=0.0)
    net.step((1.1, 0.0))
    net.step((0.0, 1.1))
    assert net.synapses[0].weight == 0.5


def test_reset_preserves_weights_and_clears_activity():
    net = SpikingCircuit(2, [Synapse(0, 1, 0.5)], leak=0.0)
    net.step((1.1, 0.0), learn=True)
    net.step((0.0, 1.1), learn=True)
    weight = net.synapses[0].weight
    net.reset_activity()
    assert net.synapses[0].weight == weight
    assert net.pending == [0.0, 0.0]
    assert net.synapses[0].pre_trace == 0.0


@pytest.mark.parametrize("bad", [float("nan"), float("inf")])
def test_nonfinite_current_rejected(bad):
    net = SpikingCircuit(1, [])
    with pytest.raises(ValueError):
        net.step((bad,))


def test_invalid_connectivity_rejected():
    with pytest.raises(ValueError):
        SpikingCircuit(2, [Synapse(0, 2, 0.5)])
