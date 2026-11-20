"""Small, deterministic leaky integrate-and-fire (LIF) circuit with pair-based STDP.

Research prototype: synthetic connectivity, not FAFB-derived physiology.
Time steps are dimensionless. All inputs and parameters are explicitly synthetic.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite


@dataclass
class Synapse:
    pre: int
    post: int
    weight: float
    pre_trace: float = 0.0
    post_trace: float = 0.0


class SpikingCircuit:
    """Discrete LIF neurons with bounded excitatory STDP.

    Inputs are injected current per step; synaptic events from step t are
    delivered at step t+1. Traces decay before new events are processed.
    """

    def __init__(
        self, neuron_count: int, synapses: list[Synapse], *,
        leak: float = 0.8, threshold: float = 1.0,
        trace_decay: float = 0.8, learning_rate: float = 0.05,
        max_weight: float = 2.0,
    ) -> None:
        if neuron_count < 1 or not (0 <= leak < 1) or threshold <= 0:
            raise ValueError("invalid neuron parameters")
        if not (0 <= trace_decay < 1) or learning_rate < 0 or max_weight <= 0:
            raise ValueError("invalid plasticity parameters")
        if not all(isfinite(x) for x in (leak, threshold, trace_decay, learning_rate, max_weight)):
            raise ValueError("parameters must be finite")
        self.neuron_count = neuron_count
        self.synapses = [Synapse(s.pre, s.post, s.weight) for s in synapses]
        for s in self.synapses:
            if not (0 <= s.pre < neuron_count and 0 <= s.post < neuron_count):
                raise ValueError("synapse endpoint outside circuit")
            if not isfinite(s.weight) or not 0 <= s.weight <= max_weight:
                raise ValueError("synaptic weight outside bounds")
        self.leak = leak
        self.threshold = threshold
        self.trace_decay = trace_decay
        self.learning_rate = learning_rate
        self.max_weight = max_weight
        self.voltage = [0.0] * neuron_count
        self.pending = [0.0] * neuron_count

    def step(self, current: tuple[float, ...], *, learn: bool = False) -> tuple[bool, ...]:
        if len(current) != self.neuron_count or not all(isfinite(x) for x in current):
            raise ValueError("current must contain one finite value per neuron")
        spikes = []
        for i, drive in enumerate(current):
            voltage = self.leak * self.voltage[i] + drive + self.pending[i]
            fired = voltage >= self.threshold
            self.voltage[i] = 0.0 if fired else voltage
            spikes.append(fired)
        events = tuple(spikes)
        self.pending = [0.0] * self.neuron_count
        for syn in self.synapses:
            old_pre = syn.pre_trace * self.trace_decay
            old_post = syn.post_trace * self.trace_decay
            # Causal pre-before-post potentiates; post-before-pre depresses.
            if learn:
                delta = self.learning_rate * (
                    (old_pre if events[syn.post] else 0.0)
                    - (old_post if events[syn.pre] else 0.0)
                )
                syn.weight = min(self.max_weight, max(0.0, syn.weight + delta))
            syn.pre_trace = old_pre + float(events[syn.pre])
            syn.post_trace = old_post + float(events[syn.post])
            if events[syn.pre]:
                self.pending[syn.post] += syn.weight
        return events

    def reset_activity(self) -> None:
        """Reset activity/traces without forgetting learned synaptic weights."""
        self.voltage = [0.0] * self.neuron_count
        self.pending = [0.0] * self.neuron_count
        for syn in self.synapses:
            syn.pre_trace = 0.0
            syn.post_trace = 0.0


def timing_experiment() -> dict[str, object]:
    """Compare causal and anti-causal synthetic spike timing."""
    def run(pre_first: bool) -> float:
        net = SpikingCircuit(2, [Synapse(0, 1, 0.5)], leak=0.0)
        sequence = ((1.1, 0.0), (0.0, 1.1)) if pre_first else (
            (0.0, 1.1), (1.1, 0.0)
        )
        for stimulus in sequence:
            net.step(stimulus, learn=True)
        return net.synapses[0].weight

    return {
        "circuit": "synthetic_two_neuron_lif_stdp",
        "connectome_derived": False,
        "biologically_validated": False,
        "initial_weight": 0.5,
        "causal_weight": run(True),
        "anticausal_weight": run(False),
    }
