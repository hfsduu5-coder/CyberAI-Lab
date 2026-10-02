from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable
from .analyzers import headers_report, log_summary, parse_http_request, recon_report

Analyzer=Callable[[str],Any]
@dataclass(frozen=True)
class Module:
    name:str
    description:str
    analyzer:Analyzer
    ai_prompt:str
_REGISTRY={}

def register(module):
    if not module.name or not module.name.replace("-","").isalnum(): raise ValueError("Invalid module name.")
    if module.name in _REGISTRY: raise ValueError(f"Module already registered: {module.name}")
    _REGISTRY[module.name]=module

def get_module(name):
    try: return _REGISTRY[name]
    except KeyError as exc: raise ValueError(f"Unknown module: {name}") from exc

def list_modules(): return sorted(_REGISTRY.values(),key=lambda x:x.name)

register(Module("http","Parse a saved HTTP request offline.",parse_http_request,"Review this HTTP metadata from an authorized lab. Do not invent vulnerabilities."))
register(Module("recon","Summarize saved reconnaissance output offline.",recon_report,"Review this offline recon summary. Separate evidence from hypotheses."))
register(Module("headers","Review saved HTTP response headers offline.",headers_report,"Review these saved response-header observations defensively. Missing headers are signals, not proof of a vulnerability."))
register(Module("logs","Summarize saved application/security logs offline.",log_summary,"Review this offline log summary. Highlight supported observations and defensive follow-up questions."))
