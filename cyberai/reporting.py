from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def build_report(kind: str, source: str, data: Any) -> dict:
    return {"schema_version": 1, "generated_at": datetime.now(timezone.utc).isoformat(), "kind": kind, "source": source, "data": data}

def save_report(report: dict, output: str, fmt: str) -> Path:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "json":
        content = json.dumps(report, indent=2, ensure_ascii=False)
    elif fmt == "md":
        data = report.get("data", "")
        rendered = json.dumps(data, indent=2, ensure_ascii=False) if isinstance(data, (dict, list)) else str(data)
        content = "# CyberAI-Lab Report\n\n**Type:** " + str(report.get("kind","")) + "\n\n**Source:** " + str(report.get("source","")) + "\n\n**Generated:** " + str(report.get("generated_at","")) + "\n\n## Results\n\n" + rendered + "\n"
    else:
        raise ValueError("Report format must be 'json' or 'md'.")
    path.write_text(content, encoding="utf-8")
    return path
