from dataclasses import FrozenInstanceError

import pytest

from cortex.contracts import (
    BrainInstanceId,
    BrainResult,
    EvidenceStatus,
    TaskEnvelope,
)


def test_four_instance_ids_are_explicit_and_stable():
    assert [instance.value for instance in BrainInstanceId] == ["C1", "C2", "C3", "C4"]


def test_task_envelope_defaults_and_target():
    task = TaskEnvelope(
        task_id="task-001",
        task_type="synthetic-smoke-test",
        target_instance=BrainInstanceId.PERCEPTION,
    )
    assert task.payload == {}
    assert task.target_instance is BrainInstanceId.PERCEPTION
    with pytest.raises(FrozenInstanceError):
        task.task_id = "mutated"


@pytest.mark.parametrize("task_id,task_type", [("", "x"), ("   ", "x"), ("x", ""), ("x", "  ")])
def test_task_envelope_rejects_empty_identifiers(task_id, task_type):
    with pytest.raises(ValueError):
        TaskEnvelope(task_id=task_id, task_type=task_type)


def test_brain_result_preserves_evidence_and_provenance():
    result = BrainResult(
        task_id="task-001",
        instance_id=BrainInstanceId.LEARNING,
        output={"learned": False},
        evidence_status=EvidenceStatus.HYPOTHESIS,
        confidence=0.4,
        source_refs=("fixture://synthetic-01",),
        memory_version_read=0,
    )
    assert result.evidence_status is EvidenceStatus.HYPOTHESIS
    assert result.source_refs == ("fixture://synthetic-01",)
    assert result.memory_version_read == 0


@pytest.mark.parametrize("confidence", [-0.01, 1.01])
def test_brain_result_rejects_invalid_confidence(confidence):
    with pytest.raises(ValueError):
        BrainResult(task_id="t", instance_id=BrainInstanceId.COORDINATOR, confidence=confidence)


def test_brain_result_rejects_invalid_provenance_and_memory_version():
    with pytest.raises(ValueError):
        BrainResult(task_id="t", instance_id=BrainInstanceId.ACTION, source_refs=("",))
    with pytest.raises(ValueError):
        BrainResult(task_id="t", instance_id=BrainInstanceId.ACTION, memory_version_read=-1)
