import io
import json
import pytest
from unittest.mock import patch
from cortex.coding_agent.ollama import OllamaProvider
from cortex.coding_agent import CodingAgent, ExperienceStore

class FakeResponse:
    def __init__(self, content):
        self.stream = io.BytesIO(json.dumps(content).encode())
    def __enter__(self):
        return self.stream
    def __exit__(self, *args):
        self.stream.close()

def test_ollama_adapter_and_agent(tmp_path):
    provider = OllamaProvider(model="qwen3:8b")
    def fake_open(request, timeout):
        body = json.loads(request.data)
        assert body["model"] == "qwen3:8b"
        assert body["stream"] is False
        assert "hello" in body["prompt"]
        assert timeout == 120
        return FakeResponse({"response": "print('hello')"})
    with patch("cortex.coding_agent.ollama.urlopen", side_effect=fake_open):
        agent = CodingAgent(provider, ExperienceStore(tmp_path / "history.json"))
        assert agent.propose("hello").candidate == "print('hello')"

def test_no_nonlocal_endpoint():
    for endpoint in ["https://example.com/api/generate", "http://192.168.1.2:11434/api/generate", "http://127.0.0.1:11434/admin", "http://localhost:11434/api/generate?x=1"]:
        with pytest.raises(ValueError):
            OllamaProvider(endpoint=endpoint)

def test_invalid_response():
    with patch("cortex.coding_agent.ollama.urlopen", return_value=FakeResponse({"response": ""})):
        with pytest.raises(ValueError):
            OllamaProvider()("test")
