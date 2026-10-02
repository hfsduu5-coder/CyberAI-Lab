from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Any

from .analyzers import parse_http_request, recon_report


Analyzer = Callable[[str], Any]


@dataclass(frozen=True)
class Module:
    name: str
    description: str
    analyzer: Analyzer
    ai_prompt: str


_REGISTRY: dict[str, Module] = {}


def register(module: Module) -> None:
    if not module.name or not module.name.replace("-", "").isalnum():
        raise ValueError("Module name must contain only letters, numbers, or hyphens.")
    if module.name in _REGISTRY:
        raise ValueError(f"Module already registered: {module.name}")
    _REGISTRY[module.name] = module


def get_module(name: str) -> Module:
    try:
        return _REGISTRY[name]
    except KeyError as exc:
        raise ValueError(f"Unknown module: {name}") from exc


def list_modules() -> list[Module]:
    return sorted(_REGISTRY.values(), key=lambda item: item.name)


register(Module(
    name="http",
    description="Parse a saved HTTP request offline.",
    analyzer=parse_http_request,
    ai_prompt=(
        "Review this HTTP request metadata from an authorized lab. "
        "Do not invent vulnerabilities. Explain supported security observations "
        "and safe validation questions."
    ),
))

register(Module(
    name="recon",
    description="Summarize saved reconnaissance output offline.",
    analyzer=recon_report,
    ai_prompt=(
        "Review this offline summary of supplied reconnaissance output. "
        "Separate evidence from hypotheses and suggest authorized next validation steps."
    ),
))
