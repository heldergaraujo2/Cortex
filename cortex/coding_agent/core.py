"""Three-stage coding agent scaffold: provider, experience, guarded improvement.

The caller owns model execution and test execution. This module never runs arbitrary
code, fetches the internet, or edits its own source without explicit integration.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable
import json

@dataclass(frozen=True)
class Proposal:
    task: str
    candidate: str
    feedback: str = ""

class ExperienceStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def read(self) -> list[dict]:
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("Experience store must contain a JSON list")
        return data

    def append(self, record: dict) -> None:
        records = self.read()
        records.append(record)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.path)

class CodingAgent:
    def __init__(self, generate: Callable[[str], str], store: ExperienceStore):
        self.generate = generate  # injected provider, e.g. local Qwen adapter
        self.store = store

    def propose(self, task: str) -> Proposal:
        if not task.strip():
            raise ValueError("Task cannot be empty")
        history = self.store.read()[-5:]
        prompt = "Write a proposed code solution. Do not execute it.\\nTask: " + task
        if history:
            prompt += "\\nPrior verified experiences:\\n" + json.dumps(history, ensure_ascii=False)
        return Proposal(task=task, candidate=self.generate(prompt))

    def evaluate(self, proposal: Proposal, verify: Callable[[str], tuple[bool, str]]) -> bool:
        # verify must run in a separately configured sandbox; no built-in shell access
        passed, feedback = verify(proposal.candidate)
        self.store.append({"task": proposal.task, "candidate": proposal.candidate,
                           "passed": bool(passed), "feedback": str(feedback)})
        return bool(passed)

    def propose_improvement(self, source: str, objective: str) -> Proposal:
        # A proposal only. No direct modification of live agent source.
        prompt = ("Suggest a minimal source patch to improve the following objective. "
                  "Do not apply changes.\\nObjective: " + objective + "\\nSource:\\n" + source)
        return Proposal(task="self-improvement: " + objective, candidate=self.generate(prompt))

    @staticmethod
    def accept_improvement(baseline_score: float, candidate_score: float,
                           tests_passed: bool, human_approved: bool) -> bool:
        return bool(tests_passed and human_approved and candidate_score > baseline_score)
