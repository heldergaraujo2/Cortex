"""Targeted persistent skill-memory checks."""
import json

import pytest

from cortex.experiments.skill_memory import Skill, SkillMemory


def test_skill_survives_new_memory_instance(tmp_path):
    path = tmp_path / "skills.json"
    memory = SkillMemory(path)
    memory.save(Skill("make_cube", ("open Blender", "add cube", "save file"), "fixture://verified"))
    restarted = SkillMemory(path)
    assert restarted.recall("make_cube").steps == ("open Blender", "add cube", "save file")


def test_multiple_skills_and_replacement(tmp_path):
    memory = SkillMemory(tmp_path / "skills.json")
    memory.save(Skill("a", ("first",), "test://1"))
    memory.save(Skill("b", ("second",), "test://2"))
    memory.save(Skill("a", ("updated",), "test://3"))
    assert list(memory.load()) == ["a", "b"]
    assert memory.recall("a").steps == ("updated",)


def test_missing_skill(tmp_path):
    assert SkillMemory(tmp_path / "missing.json").recall("x") is None


@pytest.mark.parametrize("name,steps,evidence", [
    ("", ("step",), "test://1"),
    ("valid", (), "test://1"),
    ("valid", ("",), "test://1"),
    ("valid", ("step",), ""),
])
def test_invalid_skills_rejected(name, steps, evidence):
    with pytest.raises(ValueError):
        Skill(name, steps, evidence)


def test_corrupted_file_fails_without_silent_reset(tmp_path):
    path = tmp_path / "skills.json"
    path.write_text("{bad json", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        SkillMemory(path).save(Skill("a", ("step",), "test://1"))
    assert path.read_text(encoding="utf-8") == "{bad json"


def test_unsupported_schema_rejected(tmp_path):
    path = tmp_path / "skills.json"
    path.write_text('{"schema_version":2,"skills":[]}', encoding="utf-8")
    with pytest.raises(ValueError, match="schema"):
        SkillMemory(path).load()
