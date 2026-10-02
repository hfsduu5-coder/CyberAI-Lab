from __future__ import annotations
import html
import json
from pathlib import Path
from .modules import list_modules
from .workspace import workspace_status

def _card(title: str, value: str) -> str:
    return f'<div class="card"><span>{html.escape(title)}</span><strong>{html.escape(value)}</strong></div>'

def build_dashboard(root: str = "workspaces") -> str:
    base=Path(root)
    workspaces=[]
    if base.exists():
        for item in sorted(base.iterdir()):
            if item.is_dir() and (item/"workspace.json").is_file():
                try: workspaces.append(workspace_status(str(item)))
                except ValueError: pass
    modules=list_modules()
    total_reports=sum(w["reports"] for w in workspaces)
    total_inputs=sum(w["inputs"] for w in workspaces)
    rows="".join(
        f"<tr><td>{html.escape(Path(w['workspace']).name)}</td><td>{w['inputs']}</td><td>{w['reports']}</td><td>{w['notes']}</td></tr>"
        for w in workspaces
    ) or '<tr><td colspan="4">No local workspaces found.</td></tr>'
    module_items="".join(f"<li><b>{html.escape(m.name)}</b><span>{html.escape(m.description)}</span></li>" for m in modules)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CyberAI-Lab Dashboard</title>
<style>
:root{{--bg:#080a0d;--panel:#12161c;--line:#252b34;--text:#edf0f4;--muted:#9ca6b5;--accent:#8b1e3f}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font-family:Inter,system-ui,sans-serif}}
main{{max-width:1100px;margin:auto;padding:44px 22px}}header{{margin-bottom:28px}}h1{{font-size:34px;margin:0 0 8px}}p{{color:var(--muted)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin:24px 0}}
.card,.panel{{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:20px}}
.card span{{display:block;color:var(--muted);font-size:13px}}.card strong{{display:block;font-size:30px;margin-top:8px}}
.panel{{margin-top:18px}}table{{width:100%;border-collapse:collapse}}th,td{{padding:12px;text-align:left;border-bottom:1px solid var(--line)}}th{{color:var(--muted)}}
ul{{list-style:none;padding:0}}li{{display:flex;gap:18px;padding:10px 0;border-bottom:1px solid var(--line)}}li b{{min-width:90px;color:#fff}}li span{{color:var(--muted)}}
.badge{{display:inline-block;background:var(--accent);padding:5px 10px;border-radius:999px;font-size:12px}}
</style></head><body><main>
<header><span class="badge">LOCAL • OFFLINE VIEW</span><h1>CyberAI-Lab Dashboard</h1><p>Read-only overview of local workspaces and installed analysis modules.</p></header>
<div class="grid">{_card("Workspaces",str(len(workspaces)))}{_card("Inputs",str(total_inputs))}{_card("Reports",str(total_reports))}{_card("Modules",str(len(modules)))}</div>
<section class="panel"><h2>Workspaces</h2><table><thead><tr><th>Name</th><th>Inputs</th><th>Reports</th><th>Notes</th></tr></thead><tbody>{rows}</tbody></table></section>
<section class="panel"><h2>Analyzer Modules</h2><ul>{module_items}</ul></section>
</main></body></html>"""

def save_dashboard(output: str, root: str = "workspaces") -> Path:
    path=Path(output); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(build_dashboard(root),encoding="utf-8")
    return path
