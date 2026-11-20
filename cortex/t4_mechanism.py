"""Exploratory signed-input model for a single T4-like unit.

This is a dimensionless rate-level experiment, not a calibrated biological
model. Spatial receptive-field offsets and temporal parameters are explicit
engineering hypotheses and must not be read as FAFB measurements.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True, slots=True)
class T4InputArm:
    name: str
    source_types: tuple[str, ...]
    transmitter_label: str
    synaptic_sign: int
    response_polarity: int
    receptive_position: int
    tau_steps: float
    delay_steps: int
    gain: float

    def validate(self) -> None:
        if not self.name.strip() or not self.source_types:
            raise ValueError("arm name and source_types must be non-empty")
        if self.synaptic_sign not in {-1, 1}:
            raise ValueError("synaptic_sign must be -1 or +1")
        if self.response_polarity not in {-1, 1}:
            raise ValueError("response_polarity must be -1 or +1")
        if not isinstance(self.receptive_position, int):
            raise ValueError("receptive_position must be an integer")
        if not isfinite(self.tau_steps) or self.tau_steps < 1:
            raise ValueError("tau_steps must be finite and >= 1")
        if not isinstance(self.delay_steps, int) or self.delay_steps < 0:
            raise ValueError("delay_steps must be an integer >= 0")
        if not isfinite(self.gain) or self.gain < 0:
            raise ValueError("gain must be finite and >= 0")


@dataclass(frozen=True, slots=True)
class T4MechanismConfig:
    leak: float = 0.7
    maximum_rate: float = 1.0

    def validate(self) -> None:
        if not isfinite(self.leak) or not 0 <= self.leak <= 1:
            raise ValueError("leak must be finite and within [0, 1]")
        if not isfinite(self.maximum_rate) or self.maximum_rate <= 0:
            raise ValueError("maximum_rate must be finite and > 0")


def default_t4_input_arms() -> tuple[T4InputArm, ...]:
    """Return literature-informed channel hypotheses with uncalibrated offsets."""
    return (
        T4InputArm(
            "fast_cholinergic_excitation", ("Mi1", "Tm3"), "ACH",
            synaptic_sign=1, response_polarity=1, receptive_position=0,
            tau_steps=1.0, delay_steps=0, gain=1.0,
        ),
        T4InputArm(
            "slow_gabaergic_inhibition", ("Mi4", "C3", "CT1", "TmY15"), "GABA",
            synaptic_sign=-1, response_polarity=1, receptive_position=1,
            tau_steps=3.0, delay_steps=1, gain=0.8,
        ),
        T4InputArm(
            "mi9_glutamatergic_disinhibition", ("Mi9",), "GLUT",
            synaptic_sign=-1, response_polarity=-1, receptive_position=-1,
            tau_steps=3.0, delay_steps=1, gain=0.35,
        ),
    )


def run_t4_mechanism(
    stimulus_positions: tuple[int, ...],
    arms: tuple[T4InputArm, ...] | None = None,
    config: T4MechanismConfig = T4MechanismConfig(),
) -> dict[str, object]:
    """Simulate signed, filtered input channels for one moving ON bar.

    Each integer in stimulus_positions is the bar position at one abstract
    step. Positive/negative source polarity is a response deviation around a
    baseline, not a negative firing rate. The output is clipped and therefore
    remains a bounded rate-like engineering variable.
    """
    if not stimulus_positions:
        raise ValueError("stimulus_positions must not be empty")
    if any(not isinstance(position, int) for position in stimulus_positions):
        raise ValueError("stimulus positions must be integers")
    config.validate()
    selected_arms = arms if arms is not None else default_t4_input_arms()
    if not selected_arms:
        raise ValueError("at least one input arm is required")
    names = [arm.name for arm in selected_arms]
    if len(names) != len(set(names)):
        raise ValueError("input arm names must be unique")
    for arm in selected_arms:
        arm.validate()

    filtered = {arm.name: 0.0 for arm in selected_arms}
    queues = {arm.name: [0.0] * arm.delay_steps for arm in selected_arms}
    arm_traces = {arm.name: [] for arm in selected_arms}
    rate = 0.0
    rate_trace: list[float] = []
    net_drive_trace: list[float] = []

    for position in stimulus_positions:
        net_drive = 0.0
        for arm in selected_arms:
            raw = (
                float(arm.response_polarity)
                if position == arm.receptive_position else 0.0
            )
            alpha = 1.0 / arm.tau_steps
            filtered[arm.name] += alpha * (raw - filtered[arm.name])
            if arm.delay_steps:
                queues[arm.name].append(filtered[arm.name])
                signal = queues[arm.name].pop(0)
            else:
                signal = filtered[arm.name]
            drive = signal * arm.synaptic_sign * arm.gain
            arm_traces[arm.name].append(drive)
            net_drive += drive
        rate = min(config.maximum_rate, max(0.0, config.leak * rate + net_drive))
        rate_trace.append(rate)
        net_drive_trace.append(net_drive)

    peak = max(rate_trace, default=0.0)
    return {
        "model": "synthetic-signed-rate-level-T4-mechanism-v1",
        "steps": len(stimulus_positions),
        "stimulus_positions": list(stimulus_positions),
        "configuration": {
            "leak": config.leak,
            "maximum_rate": config.maximum_rate,
            "time_unit": "abstract simulation step; not biological time",
        },
        "arms": [
            {
                "name": arm.name,
                "source_types": list(arm.source_types),
                "transmitter_label": arm.transmitter_label,
                "synaptic_sign": arm.synaptic_sign,
                "response_polarity": arm.response_polarity,
                "receptive_position": arm.receptive_position,
                "tau_steps": arm.tau_steps,
                "delay_steps": arm.delay_steps,
                "gain": arm.gain,
                "parameter_status": "literature-informed engineering hypothesis; not calibrated",
            }
            for arm in selected_arms
        ],
        "metrics": {
            "peak_rate": peak,
            "integrated_rate": sum(rate_trace),
            "rate_trace": rate_trace,
            "net_drive_trace": net_drive_trace,
            "arm_drive_traces": arm_traces,
        },
        "interpretation_limit": (
            "Synthetic one-dimensional receptive-field demonstration only. Positions, gains, "
            "filters and delays are engineering hypotheses; no FAFB cell-level spatial mapping, "
            "biological time calibration, preferred/null direction label or biological DSI is used."
        ),
    }


def compare_opposite_sweeps(
    extent: int = 2,
    arms: tuple[T4InputArm, ...] | None = None,
    config: T4MechanismConfig = T4MechanismConfig(),
) -> dict[str, object]:
    if not isinstance(extent, int) or extent < 1:
        raise ValueError("extent must be an integer >= 1")
    forward = tuple(range(-extent, extent + 1))
    reverse = tuple(reversed(forward))
    plus = run_t4_mechanism(forward, arms, config)
    minus = run_t4_mechanism(reverse, arms, config)
    r_plus = plus["metrics"]["integrated_rate"]
    r_minus = minus["metrics"]["integrated_rate"]
    denominator = r_plus + r_minus
    asymmetry = (r_plus - r_minus) / denominator if denominator else 0.0
    return {
        "experiment": "synthetic-opposite-sweeps-T4-mechanism-v1",
        "forward": plus,
        "reverse": minus,
        "comparison": {
            "same_stimulus_event_count": len(forward) == len(reverse),
            "forward_integrated_rate": r_plus,
            "reverse_integrated_rate": r_minus,
            "synthetic_directional_asymmetry_index": asymmetry,
            "biological_dsi_claimed": False,
        },
    }
