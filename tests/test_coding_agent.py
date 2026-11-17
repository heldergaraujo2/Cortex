from cortex.coding_agent import CodingAgent, ExperienceStore


def test_three_stages(tmp_path):
    prompts = []
    def generate(prompt):
        prompts.append(prompt)
        return "print('hello')"
    agent = CodingAgent(generate, ExperienceStore(tmp_path / "experience.json"))
    first = agent.propose("write a hello world program")
    assert first.candidate == "print('hello')"
    assert agent.evaluate(first, lambda code: (code == "print('hello')", "verified in sandbox"))
    second = agent.propose("write another program")
    assert "Prior verified experiences" in prompts[-1]
    assert agent.propose_improvement("x=1", "readability").candidate
    assert not agent.accept_improvement(0.5, 0.8, True, False)
    assert not agent.accept_improvement(0.5, 0.4, True, True)
    assert agent.accept_improvement(0.5, 0.8, True, True)


def test_reject_empty_task(tmp_path):
    import pytest
    agent = CodingAgent(lambda _: "", ExperienceStore(tmp_path / "history.json"))
    with pytest.raises(ValueError):
        agent.propose(" ")
