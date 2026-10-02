from __future__ import annotations
import argparse
import json
from .analyzers import read_text
from .config import load_settings
from .modules import get_module, list_modules
from .providers import ProviderError, complete
from .reporting import build_report, save_report
from .workspace import create_workspace, workspace_status

def ask_ai(prompt):
    s=load_settings()
    messages=[{"role":"system","content":s.system_prompt},{"role":"user","content":prompt}]
    print(complete(s,messages))
    return 0

def emit(kind, source, data, output, fmt):
    if output:
        p=save_report(build_report(kind,source,data),output,fmt)
        print(f"Report saved: {p}")
    else:
        print(json.dumps(data,indent=2,ensure_ascii=False) if isinstance(data,(dict,list)) else data)

def run_module(name,path,use_ai,output,fmt):
    module=get_module(name)
    data=module.analyzer(read_text(path))
    if use_ai:
        rendered=json.dumps(data,ensure_ascii=False) if isinstance(data,(dict,list)) else str(data)
        return ask_ai(module.ai_prompt+"\n\n"+rendered)
    emit(name,path,data,output,fmt)
    return 0

def run_chat():
    s=load_settings()
    history=[{"role":"system","content":s.system_prompt}]
    print(f"CyberAI-Lab | provider={s.provider} | model={s.model}")
    print("Type /exit to quit or /clear to reset.")
    while True:
        try:
            prompt=input("\nYou> ").strip()
        except (EOFError,KeyboardInterrupt):
            print()
            return 0
        if not prompt:
            continue
        if prompt.lower() in {"/exit","/quit"}:
            return 0
        if prompt.lower()=="/clear":
            history=[{"role":"system","content":s.system_prompt}]
            print("Conversation cleared.")
            continue
        history.append({"role":"user","content":prompt})
        try:
            answer=complete(s,history)
        except ProviderError as exc:
            history.pop()
            print(f"Error: {exc}")
            continue
        history.append({"role":"assistant","content":answer})
        print(f"\nAI> {answer}")

def add_report_args(p):
    p.add_argument("--ai",action="store_true")
    p.add_argument("--output")
    p.add_argument("--format",choices=("json","md"),default="json")

def build_parser():
    p=argparse.ArgumentParser(prog="cyberai",description="Extensible AI-assisted CLI for authorized cybersecurity research.")
    sub=p.add_subparsers(dest="command",required=True)
    ask=sub.add_parser("ask")
    ask.add_argument("prompt")
    analyze=sub.add_parser("analyze")
    analyze.add_argument("path")
    mod=sub.add_parser("module")
    ms=mod.add_subparsers(dest="module_command",required=True)
    ms.add_parser("list")
    run=ms.add_parser("run")
    run.add_argument("name")
    run.add_argument("path")
    add_report_args(run)
    for name in ("http","recon"):
        shortcut=sub.add_parser(name)
        shortcut.add_argument("path")
        add_report_args(shortcut)
    ws=sub.add_parser("workspace").add_subparsers(dest="workspace_command",required=True)
    new=ws.add_parser("new")
    new.add_argument("name")
    new.add_argument("--root",default="workspaces")
    status=ws.add_parser("status")
    status.add_argument("path")
    sub.add_parser("chat")
    sub.add_parser("config")
    return p

def main():
    p=build_parser()
    a=p.parse_args()
    try:
        if a.command=="ask":
            return ask_ai(a.prompt)
        if a.command=="analyze":
            return ask_ai("Analyze this authorized research material. Separate evidence from hypotheses.\n\n"+read_text(a.path))
        if a.command=="module" and a.module_command=="list":
            for m in list_modules():
                print(f"{m.name:12} {m.description}")
            return 0
        if a.command=="module" and a.module_command=="run":
            return run_module(a.name,a.path,a.ai,a.output,a.format)
        if a.command in {"http","recon"}:
            return run_module(a.command,a.path,a.ai,a.output,a.format)
        if a.command=="workspace" and a.workspace_command=="new":
            print(f"Workspace created: {create_workspace(a.name,a.root)}")
            return 0
        if a.command=="workspace" and a.workspace_command=="status":
            print(json.dumps(workspace_status(a.path),indent=2))
            return 0
        if a.command=="chat":
            return run_chat()
        if a.command=="config":
            s=load_settings()
            print(f"provider: {s.provider}\nmodel: {s.model}\nbase_url: {s.base_url}\ntimeout: {s.timeout}\napi_key_configured: {'yes' if s.api_key else 'no'}")
            return 0
    except (ValueError,ProviderError) as exc:
        p.exit(1,f"Error: {exc}\n")
    return 1

if __name__=="__main__":
    raise SystemExit(main())
