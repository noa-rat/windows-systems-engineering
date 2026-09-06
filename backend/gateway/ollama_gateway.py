from backend.gateway.ollama_client import generate


def summarize_with_ollama(text: str) -> str:
    prompt = (
        "Summarize this news article in a short, clear paragraph. "
        "Return only the summary.\n\n"
        f"{text}"
    )
    return generate(prompt)


def ask_ollama(prompt: str) -> str:
    return generate(prompt)
