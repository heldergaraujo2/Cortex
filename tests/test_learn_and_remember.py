"""Integration tests: learning, persistence, restart and reuse."""
import pytest

from cortex.experiments.learn_and_remember import learn_and_store, recall_and_evaluate
from cortex.experiments.skill_memory import Skill, SkillMemory


def test_learn_persist_restart_reuse(tmp_path):
    path = tmp_path / "memory" / "skills.json"
    result = learn_and_store(path)
    assert result == {"held_out_accuracy": 1.0, "saved": True, "dataset": "synthetic_only"}
    assert path.exists()
    # Separate call reopens the JSON file and reuses weights without training.
    assert recall_and_evaluate(path) == 1.0


def test_missing_memory_cannot_claim_recall(tmp_path):
    with pytest.raises(ValueError, match="unavailable"):
        recall_and_evaluate(tmp_path / "missing.json")


def test_unverified_skill_is_rejected(tmp_path):
    path = tmp_path / "skills.json"
    SkillMemory(path).save(
        Skill("synthetic_two_input_discrimination", ("0", "0"), "unverified")
    )
    with pytest.raises(ValueError, match="unavailable"):
        recall_and_evaluate(path)


def test_invalid_saved_weights_are_rejected(tmp_path):
    path = tmp_path / "skills.json"
    SkillMemory(path).save(
        Skill(
            "synthetic_two_input_discrimination",
            ("NaN", "0"),
            "held_out_accuracy=1.0;dataset=synthetic;not_biological",
        )
    )
    with pytest.raises(ValueError, match="weights"):
        recall_and_evaluate(path)
