import requests

from backend.config import settings
from backend.services.circuit_breaker import CircuitBreaker


_generation_breaker = CircuitBreaker("Ollama generation")
_embedding_breaker = CircuitBreaker("Ollama embedding")


def generate(prompt: str) -> str:
    _generation_breaker.before_call()
    try:
        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": settings.OLLAMA_GENERATION_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 512,
                    "temperature": 0.2,
                },
            },
            timeout=settings.OLLAMA_GENERATION_TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
        answer = payload.get("response", "").strip()
        if not answer:
            raise RuntimeError("Ollama generation returned an empty response.")
        _generation_breaker.success()
        return answer
    except (requests.RequestException, ValueError, RuntimeError):
        _generation_breaker.failure()
        raise


def embed(texts: list[str]) -> list[list[float]]:
    _embedding_breaker.before_call()
    try:
        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/embed",
            json={
                "model": settings.OLLAMA_EMBEDDING_MODEL,
                "input": texts,
            },
            timeout=settings.OLLAMA_EMBEDDING_TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
        embeddings = payload.get("embeddings")
        if not isinstance(embeddings, list) or len(embeddings) != len(texts):
            raise RuntimeError("Ollama embedding returned an invalid response.")
        _embedding_breaker.success()
        return embeddings
    except (requests.RequestException, ValueError, RuntimeError):
        _embedding_breaker.failure()
        raise
