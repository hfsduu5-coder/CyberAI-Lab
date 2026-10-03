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
    target=base / "workspace.json"
    tmp=target.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(metadata, indent=2)+"\n", encoding="utf-8")
    tmp.replace(target)
    (base / "notes" / "README.md").write_text("# Notes\n\nStore non-sensitive lab notes here. Do not commit credentials or private target data.\n", encoding="utf-8")
    return base

def workspace_status(path: str) -> dict:
    base = Path(path)
    if not base.is_dir():
        raise ValueError(f"Workspace not found: {base}")
    meta=base / "workspace.json"
    if not meta.is_file():
        raise ValueError("Not a CyberAI-Lab workspace.")
    try:
        metadata=json.loads(meta.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc:
        raise ValueError("Workspace metadata is invalid.") from exc
    def count(folder: str) -> int:
        target = base / folder
        return sum(1 for item in target.rglob("*") if item.is_file()) if target.exists() else 0
    return {"workspace": str(base), "name": metadata.get("name"), "created_at": metadata.get("created_at"), "inputs": count("inputs"), "reports": count("reports"), "notes": count("notes")}
