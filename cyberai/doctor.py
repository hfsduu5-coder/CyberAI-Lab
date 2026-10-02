from __future__ import annotations
import sys
from pathlib import Path
from .config import load_settings
from .modules import list_modules

def run_checks() -> tuple[list[dict], bool]:
    checks=[]
    checks.append({"name":"python","ok":sys.version_info >= (3,10),"detail":sys.version.split()[0]})
    try:
        settings=load_settings()
        checks.append({"name":"configuration","ok":True,"detail":f"{settings.provider} / {settings.model}"})
        if settings.provider=="ollama":
            checks.append({"name":"provider","ok":True,"detail":"Ollama configured; connectivity is not tested by doctor."})
        else:
            checks.append({"name":"provider","ok":bool(settings.api_key),"detail":"API key configured." if settings.api_key else "API key missing."})
    except ValueError as exc:
        checks.append({"name":"configuration","ok":False,"detail":str(exc)})
    checks.append({"name":"modules","ok":len(list_modules())>0,"detail":f"{len(list_modules())} module(s) registered"})
    checks.append({"name":"env-example","ok":Path(".env.example").is_file(),"detail":"found" if Path(".env.example").is_file() else "not found in current directory"})
    return checks, all(item["ok"] for item in checks)

def format_checks(checks: list[dict]) -> str:
    return "\n".join(f"[{'OK' if item['ok'] else 'FAIL'}] {item['name']}: {item['detail']}" for item in checks)
