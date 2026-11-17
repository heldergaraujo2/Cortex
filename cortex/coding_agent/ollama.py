"""Opt-in Ollama adapter using only the Python standard library.

No remote service is contacted until generate() is called. Loopback-only by default.
"""
from __future__ import annotations
import json
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

class OllamaProvider:
    def __init__(self, model: str = "qwen3:8b", endpoint: str = "http://127.0.0.1:11434/api/generate", timeout: float = 120.0):
        parsed = urlsplit(endpoint)
        if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"} or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path != "/api/generate":
            raise ValueError("Only local Ollama /api/generate endpoints are permitted")
        if not model.strip() or timeout <= 0:
            raise ValueError("Model and positive timeout required")
        self.model, self.endpoint, self.timeout = model, endpoint, timeout

    def __call__(self, prompt: str) -> str:
        payload = json.dumps({"model": self.model, "prompt": prompt, "stream": False}).encode("utf-8")
        req = Request(self.endpoint, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        with urlopen(req, timeout=self.timeout) as response:
            result = json.load(response)
        answer = result.get("response")
        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("Ollama returned an empty or invalid response")
        return answer
