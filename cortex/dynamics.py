"""Deterministic rate-based propagation baseline for the FAFB v783 pilot.

Engineering abstraction only: synapse counts are structural proxies, not calibrated
synaptic efficacies. No membrane voltage, biological time, spatial motion or plasticity.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from math import isfinite

from cortex.connectome import PilotConnectome, is_pilot_type

_ALLOWED = {("L1", "Mi1"), ("L1", "Tm3"), ("Mi1", "T4"), ("Tm3", "T4")}


@dataclass(frozen=True, slots=True)
class RateEdge:
    pre_root_id: str
    post_root_id: str
    weight: float
    syn_count: int
    pre_type: str
    post_type: str


@dataclass(frozen=True, slots=True)
class RateNetwork:
    neuropil: str
    neuron_types: dict[str, str]
    edges: tuple[RateEdge, ...]
    input_ids: tuple[str, ...]
    readout_ids: tuple[str, ...]
    readout_ids_by_subtype: dict[str, tuple[str, ...]]


@dataclass(frozen=True, slots=True)
class RateConfig:
    steps: int = 20
    stimulus_start: int = 0
    stimulus_duration: int = 2
    amplitude: float = 1.0
    leak: float = 0.5
    minimum_synapses: int = 5

    def validate(self) -> None:
        if self.steps < 1:
            raise ValueError("steps must be >= 1")
        if self.stimulus_start < 0 or self.stimulus_duration < 0:
            raise ValueError("stimulus start/duration must be >= 0")
        if self.stimulus_start + self.stimulus_duration > self.steps:
            raise ValueError("stimulus window must fit inside simulation")
        if not isfinite(self.amplitude) or not 0 <= self.amplitude <= 1:
            raise ValueError("amplitude must be finite and within [0, 1]")
        if not isfinite(self.leak) or not 0 < self.leak <= 1:
            raise ValueError("leak must be finite and within (0, 1]")
        if self.minimum_synapses < 1:
            raise ValueError("minimum_synapses must be >= 1")


def _group(cell_type: str) -> str | None:
    if cell_type in {"L1", "Mi1", "Tm3"}:
        return cell_type
    return "T4" if cell_type.startswith("T4") else None


def build_rate_network(
    connectome: PilotConnectome,
    neuropil: str,
    minimum_synapses: int = 5,
    ablate_type: str | None = None,
) -> RateNetwork:
    """Build one neuropil-specific graph; never aggregate across neuropils."""
    if not neuropil.strip():
        raise ValueError("neuropil must be a non-empty exact label")
    if minimum_synapses < 1:
        raise ValueError("minimum_synapses must be >= 1")
    if ablate_type not in {None, "Mi1", "Tm3"}:
        raise ValueError("ablate_type must be None, 'Mi1', or 'Tm3'")

    full_neuron_types = {
        rid: kind for rid, kind in connectome.cell_types.items() if is_pilot_type(kind)
    }
    selected = []
    for edge in connectome.connections:
        if (
            edge.neuropil == neuropil
            and (_group(edge.pre_type), _group(edge.post_type)) in _ALLOWED
            and edge.syn_count >= minimum_synapses
            and edge.pre_root_id in full_neuron_types
            and edge.post_root_id in full_neuron_types
        ):
            selected.append(edge)

    # Normalize once on the intact graph. Ablations remove pathways afterwards
    # without renormalizing the remaining inputs (which would hide their loss).
    incoming_totals: dict[str, int] = defaultdict(int)
    for edge in selected:
        incoming_totals[edge.post_root_id] += edge.syn_count
    full_rate_edges = tuple(
        RateEdge(
            edge.pre_root_id, edge.post_root_id,
            edge.syn_count / incoming_totals[edge.post_root_id],
            edge.syn_count, edge.pre_type, edge.post_type,
        )
        for edge in selected
    )

    neuron_types = {
        rid: kind for rid, kind in full_neuron_types.items() if kind != ablate_type
    }
    rate_edges = tuple(
        edge for edge in full_rate_edges
        if edge.pre_root_id in neuron_types and edge.post_root_id in neuron_types
    )
    input_ids = tuple(sorted(rid for rid, kind in neuron_types.items() if kind == "L1"))
    # Keep the same T4 readout population in every ablation, including cells
    # that lose all modeled inputs. Their zero response is part of the result.
    by_subtype = {
        subtype: tuple(sorted(
            rid for rid, kind in neuron_types.items() if kind == subtype
        ))
        for subtype in ("T4a", "T4b", "T4c", "T4d")
    }
    readout_ids = tuple(sorted(rid for ids in by_subtype.values() for rid in ids))
    return RateNetwork(
        neuropil, neuron_types, rate_edges, input_ids, readout_ids, by_subtype
    )


def run_rate_simulation(
    network: RateNetwork,
    config: RateConfig = RateConfig(),
    stimulus: bool = True,
) -> dict[str, object]:
    """Run synchronous deterministic rate updates and return compact metrics."""
    config.validate()
    neuron_ids = tuple(sorted(network.neuron_types))
    incoming: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for edge in network.edges:
        incoming[edge.post_root_id].append((edge.pre_root_id, edge.weight))

    state = {rid: 0.0 for rid in neuron_ids}
    input_set = set(network.input_ids)
    trace: list[float] = []
    subtype_trace = {kind: [] for kind, ids in network.readout_ids_by_subtype.items() if ids}
    for step in range(config.steps):
        active = stimulus and config.stimulus_start <= step < (
            config.stimulus_start + config.stimulus_duration
        )
        next_state = {}
        for rid in neuron_ids:
            drive = sum(state[src] * weight for src, weight in incoming[rid])
            if active and rid in input_set:
                drive += config.amplitude
            drive = min(1.0, max(0.0, drive))
            next_state[rid] = (1.0 - config.leak) * state[rid] + config.leak * drive
        state = next_state
        trace.append(
            sum(state[rid] for rid in network.readout_ids) / len(network.readout_ids)
            if network.readout_ids else 0.0
        )
        for subtype, ids in network.readout_ids_by_subtype.items():
            if ids:
                subtype_trace[subtype].append(sum(state[rid] for rid in ids) / len(ids))

    peak = max(trace, default=0.0)
    return {
        "stimulus": {
            "enabled": stimulus,
            "start_step": config.stimulus_start,
            "duration_steps": config.stimulus_duration if stimulus else 0,
            "amplitude": config.amplitude if stimulus else 0.0,
        },
        "metrics": {
            "readout_neurons": len(network.readout_ids),
            "peak_mean_t4_rate": peak,
            "peak_step": trace.index(peak) if trace else None,
            "mean_t4_rate_over_steps": sum(trace) / len(trace) if trace else 0.0,
            "t4_rate_trace": trace,
            "t4_subtype_mean_rate_traces": subtype_trace,
        },
    }


def run_baseline_experiment(
    connectome: PilotConnectome,
    neuropil: str,
    config: RateConfig = RateConfig(),
) -> dict[str, object]:
    """Run pulse, no-input control and Mi1/Tm3 pathway ablations."""
    config.validate()
    scenarios = {}
    for label, ablation, stimulated in (
        ("pulse", None, True),
        ("no_stimulus", None, False),
        ("pulse_without_Mi1", "Mi1", True),
        ("pulse_without_Tm3", "Tm3", True),
    ):
        network = build_rate_network(
            connectome, neuropil, config.minimum_synapses, ablation
        )
        result = run_rate_simulation(network, config, stimulated)
        scenarios[label] = {
            "ablation": ablation,
            "network": {
                "neuropil": network.neuropil,
                "neurons": len(network.neuron_types),
                "edges": len(network.edges),
                "l1_input_neurons": len(network.input_ids),
                "t4_readout_neurons": len(network.readout_ids),
                "t4_readout_neurons_with_incoming_edges": len({
                    edge.post_root_id for edge in network.edges
                    if edge.post_root_id in set(network.readout_ids)
                }),
                "t4_readout_by_subtype": {
                    kind: len(ids) for kind, ids in network.readout_ids_by_subtype.items()
                },
                "t4_readout_connected_by_subtype": {
                    kind: len({
                        edge.post_root_id for edge in network.edges
                        if edge.post_root_id in set(ids)
                    })
                    for kind, ids in network.readout_ids_by_subtype.items()
                },
                "synapse_count_threshold": config.minimum_synapses,
            },
            **result,
        }

    pulse = scenarios["pulse"]["metrics"]
    control = scenarios["no_stimulus"]["metrics"]
    return {
        "experiment": "fafb-v783-structural-rate-baseline-v0",
        "dataset": "FlyWire FAFB v783",
        "model": {
            "kind": "deterministic discrete-time rate propagation",
            "update": "r[t+1] = (1-leak)*r[t] + leak*clip(weighted_input, 0, 1)",
            "weight_rule": "syn_count / total incoming syn_count for each postsynaptic neuron, within selected neuropil",
            "leak": config.leak,
            "steps": config.steps,
            "minimum_synapses": config.minimum_synapses,
            "plasticity": False,
            "synapse_signs": "not modelled; all structural inputs are non-negative",
            "biophysical_calibration": False,
        },
        "comparison": {
            "pulse_minus_no_stimulus_peak": (
                pulse["peak_mean_t4_rate"] - control["peak_mean_t4_rate"]
            ),
            "direction_selectivity_claimed": False,
        },
        "scenarios": scenarios,
        "interpretation_limit": (
            "Tests deterministic propagation on a reduced directed graph only. Does not model "
            "visual space, motion direction, membrane voltage, neurotransmitter sign, biological "
            "time or learning. Synapse counts are structural proxies, not measured efficacies. "
            "Results are specific to the selected neuropil."
        ),
    }
