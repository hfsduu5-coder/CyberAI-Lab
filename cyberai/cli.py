from __future__ import annotations

import argparse
import json
from .analyzers import parse_http_request, read_text, recon_report
from .config import load_settings
from .providers import ProviderError, complete
from .reporting import build_report, save_report
from .workspace import create_workspace, workspace_status

def messages_for(prompt, system_prompt):
    return [{"role":"system","content":system_prompt},{"role":"user","content":prompt}]

def run_ask(prompt):
    s=load_settings()
    print(complete(s,messages_for(prompt,s.system_prompt)))
    return 0

def run_analyze(path):
    text=read_text(path)
    return run_ask("Analyze this authorized cybersecurity research material. Separate evidence from hypotheses and suggest safe validation steps.\n\n"+text)

def _emit(kind, source, data, output, fmt):
    if output:
        path=save_report(build_report(kind,source,data),output,fmt)
        print(f"Report saved: {path}")
    else:
        print(json.dumps(data,indent=2,ensure_ascii=False) if isinstance(data,(dict,list)) else data)

def run_http(path, ai, output, fmt):
    data=parse_http_request(read_text(path))
    if ai:
        return run_ask("Review this HTTP request metadata from an authorized lab. Do not invent vulnerabilities. Explain supported security observations and safe validation questions.\n\n"+json.dumps(data,ensure_ascii=False))
    _emit("http",path,data,output,fmt)
    return 0

def run_recon(path, ai, output, fmt):
    data=recon_report(read_text(path))
    if ai:
        return run_ask("Review this offline summary of supplied reconnaissance output. Separate evidence from hypotheses and suggest authorized next validation steps.\n\n"+data)
    _emit("recon",path,data,output,fmt)
    return 0

def run_workspace_new(name, root):
    print(f"Workspace created: {create_workspace(name,root)}")
    return 0

def run_workspace_status(path):
    print(json.dumps(workspace_status(path),indent=2))
    return 0

def run_chat():
    s=load_settings()
    history=[{"role":"system","content":s.system_prompt}]
    print(f"CyberAI-Lab | provider={s.provider} | model={s.model}")
    print("Type /exit to quit or /clear to reset the conversation.")
    while True:
        try: prompt=input("\nYou> ").strip()
        except (EOFError,KeyboardInterrupt):
            print(); return 0
        if not prompt: continue
        if prompt.lower() in {"/exit","/quit"}: return 0
        if prompt.lower()=="/clear":
            history=[{"role":"system","content":s.system_prompt}]
            print("Conversation cleared."); continue
        history.append({"role":"user","content":prompt})
        try: answer=complete(s,history)
        except ProviderError as exc:
            history.pop(); print(f"Error: {exc}"); continue
        history.append({"role":"assistant","content":answer})
        print(f"\nAI> {answer}")

def show_config():
    s=load_settings()
    print(f"provider: {s.provider}\nmodel: {s.model}\nbase_url: {s.base_url}\ntimeout: {s.timeout}\napi_key_configured: {'yes' if s.api_key else 'no'}")
    return 0

def _report_args(parser):
    parser.add_argument("--output",help="Write a report to this path.")
    parser.add_argument("--format",choices=("json","md"),default="json",help="Report format when --output is used.")

def build_parser():
    parser=argparse.ArgumentParser(prog="cyberai",description="AI-assisted CLI for authorized cybersecurity research.")
    sub=parser.add_subparsers(dest="command",required=True)
    ask=sub.add_parser("ask"); ask.add_argument("prompt")
    analyze=sub.add_parser("analyze"); analyze.add_argument("path")
    http=sub.add_parser("http",help="Parse an HTTP request offline."); http.add_argument("path"); http.add_argument("--ai",action="store_true"); _report_args(http)
    recon=sub.add_parser("recon",help="Summarize saved recon output offline."); recon.add_argument("path"); recon.add_argument("--ai",action="store_true"); _report_args(recon)
    workspace=sub.add_parser("workspace",help="Manage local lab/CTF workspaces.")
    ws=workspace.add_subparsers(dest="workspace_command",required=True)
    new=ws.add_parser("new"); new.add_argument("name"); new.add_argument("--root",default="workspaces")
    status=ws.add_parser("status"); status.add_argument("path")
    sub.add_parser("chat"); sub.add_parser("config")
    return parser

def main():
    parser=build_parser(); args=parser.parse_args()
    try:
        if args.command=="ask": return run_ask(args.prompt)
        if args.command=="analyze": return run_analyze(args.path)
        if args.command=="http": return run_http(args.path,args.ai,args.output,args.format)
        if args.command=="recon": return run_recon(args.path,args.ai,args.output,args.format)
        if args.command=="workspace" and args.workspace_command=="new": return run_workspace_new(args.name,args.root)
        if args.command=="workspace" and args.workspace_command=="status": return run_workspace_status(args.path)
        if args.command=="chat": return run_chat()
        if args.command=="config": return show_config()
    except (ValueError,ProviderError) as exc:
        parser.exit(1,f"Error: {exc}\n")
    return 1

if __name__=="__main__":
    raise SystemExit(main())
