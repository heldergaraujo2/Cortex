"""Stable, dependency-free contracts for early Cortex experiments.

These are software message contracts, not claims about biological neural states.
Dynamic neural state must remain owned by each brain instance.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping


class BrainInstanceId(str, Enum):
    """The four approved experimental brain instances."""

    COORDINATOR = "C1"
    PERCEPTION = "C2"
    LEARNING = "C3"
    ACTION = "C4"


class EvidenceStatus(str, Enum):
    """Epistemic status attached to observations and conclusions."""

    CONFIRMED = "CONFIRMADO"
    STRONGLY_INDICATED = "FORTEMENTE_INDICADO"
    HYPOTHESIS = "HIPOTESE"
    UNKNOWN = "DESCONHECIDO"


@dataclass(frozen=True, slots=True)
class TaskEnvelope:
    """Immutable task message passed through the software orchestrator."""

    task_id: str
    task_type: str
    payload: Mapping[str, object] = field(default_factory=dict)
    target_instance: BrainInstanceId | None = None
    correlation_id: str | None = None

    def __post_init__(self) -> None:
        if not self.task_id.strip():
            raise ValueError("task_id must not be empty")
        if not self.task_type.strip():
            raise ValueError("task_type must not be empty")


@dataclass(frozen=True, slots=True)
class BrainResult:
    """Result emitted by one instance without exposing its internal neural state."""

    task_id: str
    instance_id: BrainInstanceId
    output: Mapping[str, object] = field(default_factory=dict)
    evidence_status: EvidenceStatus = EvidenceStatus.UNKNOWN
    confidence: float | None = None
    source_refs: tuple[str, ...] = ()
    memory_version_read: int | None = None

    def __post_init__(self) -> None:
        if not self.task_id.strip():
            raise ValueError("task_id must not be empty")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        if self.memory_version_read is not None and self.memory_version_read < 0:
            raise ValueError("memory_version_read must be non-negative")
        if any(not ref.strip() for ref in self.source_refs):
            raise ValueError("source_refs must not contain empty references")
