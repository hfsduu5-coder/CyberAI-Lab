from __future__ import annotations
import json
import re
from datetime import datetime, timezone
from pathlib import Path

def _safe_name(name: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", name.strip()).strip("-._")
    if not value:
        raise ValueError("Workspace name must contain letters or numbers.")
    return value[:80]

def create_workspace(name: str, root: str = "workspaces") -> Path:
    safe = _safe_name(name)
    base = Path(root) / safe
    if base.exists():
        raise ValueError(f"Workspace already exists: {base}")
    for folder in ("inputs", "reports", "notes"):
        (base / folder).mkdir(parents=True, exist_ok=True)
    metadata = {"name": safe, "created_at": datetime.now(timezone.utc).isoformat(), "purpose": "Authorized cybersecurity lab / CTF / defensive research"}
    (base / "workspace.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    (base / "notes" / "README.md").write_text("# Notes\n\nStore non-sensitive lab notes here. Do not commit credentials or private target data.\n", encoding="utf-8")
    return base

def workspace_status(path: str) -> dict:
    base = Path(path)
    if not base.is_dir():
        raise ValueError(f"Workspace not found: {base}")
    def count(folder: str) -> int:
        target = base / folder
        return sum(1 for item in target.rglob("*") if item.is_file()) if target.exists() else 0
    return {"workspace": str(base), "inputs": count("inputs"), "reports": count("reports"), "notes": count("notes")}
