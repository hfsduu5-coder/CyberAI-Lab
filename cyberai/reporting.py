from __future__ import annotations
import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def build_report(kind: str, source: str, data: Any) -> dict:
    if not str(kind).strip(): raise ValueError("Report kind is required.")
    return {"schema_version":2,"generated_at":datetime.now(timezone.utc).isoformat(),"kind":str(kind).strip(),"source":Path(str(source)).name if source else "","data":data}

def _markdown(report: dict) -> str:
    data=report.get("data","")
    rendered=json.dumps(data,indent=2,ensure_ascii=False) if isinstance(data,(dict,list)) else str(data)
    return (
        "# CyberAI-Lab Report\n\n"
        f"- **Type:** {report.get('kind','')}\n"
        f"- **Source:** {report.get('source','')}\n"
        f"- **Generated:** {report.get('generated_at','')}\n\n"
        "## Results\n\n"
        f"```text\n{rendered}\n```\n"
    )

def _html(report: dict) -> str:
    data=report.get("data","")
    rendered=json.dumps(data,indent=2,ensure_ascii=False) if isinstance(data,(dict,list)) else str(data)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CyberAI-Lab Report</title>
<style>body{{font-family:system-ui,sans-serif;max-width:980px;margin:40px auto;padding:0 20px;background:#0b0d10;color:#e8eaed}}.card{{background:#15181d;border:1px solid #30343b;border-radius:14px;padding:22px}}code,pre{{white-space:pre-wrap;word-break:break-word}}.meta{{color:#aeb4bd}}h1,h2{{color:#fff}}</style></head>
<body><h1>CyberAI-Lab Report</h1><div class="card">
<p class="meta"><strong>Type:</strong> {html.escape(str(report.get("kind","")))}<br>
<strong>Source:</strong> {html.escape(str(report.get("source","")))}<br>
<strong>Generated:</strong> {html.escape(str(report.get("generated_at","")))}</p>
<h2>Results</h2><pre>{html.escape(rendered)}</pre></div></body></html>"""

def save_report(report: dict, output: str, fmt: str) -> Path:
    path=Path(output)
    if path.exists() and path.is_dir(): raise ValueError("Report output must be a file path.")
    path.parent.mkdir(parents=True,exist_ok=True)
    if fmt=="json": content=json.dumps(report,indent=2,ensure_ascii=False)
    elif fmt=="md": content=_markdown(report)
    elif fmt=="html": content=_html(report)
    else: raise ValueError("Report format must be 'json', 'md', or 'html'.")
    path.write_text(content,encoding="utf-8")
    return path
