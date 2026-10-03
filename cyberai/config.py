from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import urlparse

from dotenv import load_dotenv


DEFAULT_SYSTEM_PROMPT = (
    "You are a cybersecurity research assistant. Focus on defensive, educational, "
    "CTF, and explicitly authorized security work. Be precise, explain assumptions, "
    "and never claim evidence you do not have."
)


@dataclass(frozen=True)
class Settings:
    provider: str
    model: str
    base_url: str
    api_key: str
    timeout: int
    system_prompt: str


def load_settings() -> Settings:
    load_dotenv()

    provider = os.getenv("CYBERAI_PROVIDER", "ollama").strip().lower()
    model = os.getenv("CYBERAI_MODEL", "qwen2.5-coder").strip()
    api_key = os.getenv("CYBERAI_API_KEY", "").strip()
    timeout_raw = os.getenv("CYBERAI_TIMEOUT", "60").strip()

    if provider == "ollama":
        default_url = "http://localhost:11434"
    elif provider == "openai":
        default_url = "https://api.openai.com/v1"
    else:
        raise ValueError("CYBERAI_PROVIDER must be 'ollama' or 'openai'.")

    base_url = os.getenv("CYBERAI_BASE_URL", default_url).strip().rstrip("/")
    system_prompt = os.getenv("CYBERAI_SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT).strip()

    try:
        timeout = int(timeout_raw)
    except ValueError as exc:
        raise ValueError("CYBERAI_TIMEOUT must be an integer.") from exc

    if timeout < 1 or timeout > 300:
        raise ValueError("CYBERAI_TIMEOUT must be between 1 and 300 seconds.")
    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("CYBERAI_BASE_URL must be an absolute http(s) URL.")
    if not model:
        raise ValueError("CYBERAI_MODEL cannot be empty.")
    if provider == "openai" and not api_key:
        raise ValueError("CYBERAI_API_KEY is required when CYBERAI_PROVIDER=openai.")

    return Settings(
        provider=provider,
        model=model,
        base_url=base_url,
        api_key=api_key,
        timeout=timeout,
        system_prompt=system_prompt,
    )
