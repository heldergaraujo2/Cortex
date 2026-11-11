"""Validated synthetic learning -> durable skill memory -> recall demonstration.

This is a deterministic baseline, not autonomous skill discovery or fly-neural learning.
"""
from __future__ import annotations

from pathlib import Path

from cortex.experiments.associative import Trial, accuracy, predict, train_perceptron
from cortex.experiments.skill_memory import Skill, SkillMemory


TRAIN = (Trial((1.0, 0.0), 1), Trial((0.0, 1.0), 0))
HELD_OUT = (Trial((3.0, 0.0), 1), Trial((0.0, 3.0), 0))


def learn_and_store(path: str | Path) -> dict[str, object]:
    """Persist a deterministic classifier only after it passes held-out checks."""
    weights = train_perceptron(TRAIN, dimensions=2)
    score = accuracy(weights, HELD_OUT)
    if score != 1.0:
        raise ValueError("classifier failed validation; skill not saved")
    memory = SkillMemory(path)
    memory.save(
        Skill(
            name="synthetic_two_input_discrimination",
            steps=tuple(format(weight, ".17g") for weight in weights),
            evidence="held_out_accuracy=1.0;dataset=synthetic;not_biological",
        )
    )
    return {"held_out_accuracy": score, "saved": True, "dataset": "synthetic_only"}


def recall_and_evaluate(path: str | Path) -> float:
    """Load from disk in a fresh memory object, then reuse learned weights."""
    skill = SkillMemory(path).recall("synthetic_two_input_discrimination")
    if skill is None or skill.evidence != "held_out_accuracy=1.0;dataset=synthetic;not_biological":
        raise ValueError("validated classifier unavailable")
    if len(skill.steps) != 2:
        raise ValueError("invalid saved classifier")
    weights = tuple(float(value) for value in skill.steps)
    if not all(abs(value) < 1e6 for value in weights):
        raise ValueError("invalid saved weights")
    return accuracy(weights, HELD_OUT)
