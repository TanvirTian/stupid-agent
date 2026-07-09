import json
from typing import Any
from urllib import error, request

from config import settings


class OllamaClient:
    def __init__(self, base_url: str, model_name: str, timeout: int = 120) -> None:
        self.base_url = base_url.rstrip("/")
        self.model_name = model_name
        self.timeout = timeout

    def chat(self, user_message: str) -> str:
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            "stream": False,
        }

  
        request_body = json.dumps(payload).encode("utf-8")

        http_request = request.Request(
            url=f"{self.base_url}/api/chat",
            data=request_body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            print("Thinking...", flush=True)
            with request.urlopen(http_request, timeout=self.timeout) as response:        
                response_text = response.read().decode("utf-8")
        except error.URLError as exc:
            raise RuntimeError(
                f"Could not connect to Ollama at {self.base_url}. "
                f"Make sure Ollama is running locally. Original error: {exc}"
            ) from exc

        data: dict[str, Any] = json.loads(response_text)

        try:
            return data["message"]["content"].strip()

        except KeyError as exc:
            raise RuntimeError(f"Unexpected Ollama response format: {data}") from exc


def build_default_client() -> OllamaClient:
    return OllamaClient(
        base_url=settings.ollama_base_url,
        model_name=settings.model_name,
        timeout=settings.timeout,
    )