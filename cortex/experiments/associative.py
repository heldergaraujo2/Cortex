"""Minimal synthetic associative-learning experiment.

This is a software baseline, not a biological fly-brain reconstruction.
No FAFB connectivity or biological learning rule is claimed.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Trial:
    stimulus: tuple[float, ...]
    target: int


def predict(weights: tuple[float, ...], stimulus: tuple[float, ...]) -> int:
    if len(weights) != len(stimulus):
        raise ValueError("stimulus dimension mismatch")
    return int(sum(w * x for w, x in zip(weights, stimulus)) >= 0.0)


def accuracy(weights: tuple[float, ...], trials: tuple[Trial, ...]) -> float:
    if not trials:
        raise ValueError("trials cannot be empty")
    return sum(predict(weights, trial.stimulus) == trial.target for trial in trials) / len(trials)


def train_perceptron(
    trials: tuple[Trial, ...], *, dimensions: int, epochs: int = 12, learning_rate: float = 0.25
) -> tuple[float, ...]:
    if dimensions < 1 or epochs < 1 or learning_rate <= 0:
        raise ValueError("invalid training configuration")
    weights = [0.0] * dimensions
    for trial in trials:
        if len(trial.stimulus) != dimensions or trial.target not in (0, 1):
            raise ValueError("invalid trial")
    for _ in range(epochs):
        for trial in trials:
            error = trial.target - predict(tuple(weights), trial.stimulus)
            for index, value in enumerate(trial.stimulus):
                weights[index] += learning_rate * error * value
    return tuple(weights)


def synthetic_trials() -> tuple[Trial, ...]:
    """Toy two-input discrimination; no claim of spatial motion detection."""
    return (
        Trial((1.0, 0.0), 1),
        Trial((0.0, 1.0), 0),
        Trial((2.0, 0.0), 1),
        Trial((0.0, 2.0), 0),
    )


def run_experiment() -> dict[str, object]:
    trials = synthetic_trials()
    baseline = (0.0, 0.0)
    learned = train_perceptron(trials, dimensions=2)
    return {
        "dataset": "synthetic_only",
        "biological_validation": False,
        "baseline_accuracy": accuracy(baseline, trials),
        "trained_accuracy": accuracy(learned, trials),
        "weights": learned,
    }
