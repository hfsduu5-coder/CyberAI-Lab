from __future__ import annotations

from typing import Iterable

import requests

from .config import Settings


Message = dict[str, str]
MAX_RESPONSE_BYTES = 2_000_000


class ProviderError(RuntimeError):
    pass


def _post(url: str, *, headers: dict[str, str], payload: dict, timeout: int) -> dict:
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
        size_header=response.headers.get("Content-Length")
        if size_header:
            try:
                if int(size_header) > MAX_RESPONSE_BYTES: raise ProviderError("Provider response exceeds safety limit.")
            except ValueError:
                pass
        if len(response.content) > MAX_RESPONSE_BYTES: raise ProviderError("Provider response exceeds safety limit.")
        return response.json()
    except requests.RequestException as exc:
        raise ProviderError(f"Provider request failed: {exc}") from exc
    except ValueError as exc:
        raise ProviderError("Provider returned invalid JSON.") from exc


def complete(settings: Settings, messages: Iterable[Message]) -> str:
    items = list(messages)

    if settings.provider == "ollama":
        data = _post(
            f"{settings.base_url}/api/chat",
            headers={"Content-Type": "application/json"},
            payload={"model": settings.model, "messages": items, "stream": False},
            timeout=settings.timeout,
        )
        try:
            return data["message"]["content"].strip()
        except (KeyError, TypeError, AttributeError) as exc:
            raise ProviderError("Unexpected Ollama response format.") from exc

    headers = {
        "Authorization": f"Bearer {settings.api_key}",
        "Content-Type": "application/json",
    }
    data = _post(
        f"{settings.base_url}/chat/completions",
        headers=headers,
        payload={"model": settings.model, "messages": items},
        timeout=settings.timeout,
    )
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError, AttributeError) as exc:
        raise ProviderError("Unexpected OpenAI-compatible response format.") from exc
