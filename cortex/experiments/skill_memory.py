"""Versioned, durable storage for validated procedural skills.

A stored procedure is not neural learning; this is a controlled baseline for
reusing a skill across process restarts. No executable code is deserialized.
"""
from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Skill:
    name: str
    steps: tuple[str, ...]
    evidence: str

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.steps or any(not s.strip() for s in self.steps):
            raise ValueError("skill needs a name and nonempty steps")
        if not self.evidence.strip():
            raise ValueError("skill needs evidence of validation")


class SkillMemory:
    """Local JSON storage with atomic replacement; not safe for concurrent writers."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> dict[str, Skill]:
        if not self.path.exists():
            return {}
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("schema_version") != 1:
            raise ValueError("unsupported skill memory schema")
        raw = data.get("skills")
        if not isinstance(raw, list):
            raise ValueError("invalid skills")
        result: dict[str, Skill] = {}
        for item in raw:
            if not isinstance(item, dict) or not isinstance(item.get("steps"), list):
                raise ValueError("invalid skill entry")
            skill = Skill(
                name=item["name"],
                steps=tuple(item["steps"]),
                evidence=item["evidence"],
            )
            if skill.name in result:
                raise ValueError("duplicate skill name")
            result[skill.name] = skill
        return result

    def save(self, skill: Skill) -> None:
        skills = self.load()
        skills[skill.name] = skill
        payload = {
            "schema_version": 1,
            "skills": [
                {"name": item.name, "steps": list(item.steps), "evidence": item.evidence}
                for item in sorted(skills.values(), key=lambda s: s.name)
            ],
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=self.path.parent,
                prefix=".skill-memory-", suffix=".tmp", delete=False
            ) as handle:
                temp_path = Path(handle.name)
                json.dump(payload, handle, ensure_ascii=False, indent=2)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_path, self.path)
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)

    def recall(self, name: str) -> Skill | None:
        return self.load().get(name)
