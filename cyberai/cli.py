from __future__ import annotations

import argparse
import json

from .analyzers import read_text
from .config import load_settings
from .modules import get_module, list_modules
from .providers import ProviderError, complete
from .reporting import build_report, save_report
from .workspace import create_workspace, workspace_status


def messages_for(prompt: str, system_prompt: str) -> list[dict[str, str]]:
    return [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]


def run_ask(prompt: str) -> int:
    settings = load_settings()
    print(complete(settings, messages_for(prompt, settings.system_prompt)))
    return 0


def run_analyze(path: str) -> int:
    text = read_text(path)
    return run_ask(
        "Analyze this authorized cybersecurity research material. Separate evidence "
        "from hypotheses and suggest safe validation steps.\n\n" + text
    )


def emit(kind: str, source: str, data, output: str | None, fmt: str) -> None:
    if output:
        path = save_report(build_report(kind, source, data), output, fmt)
        print(f"Report saved: {path}")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False) if isinstance(data, (dict, list)) else data)


def run_module(name: str, path: str, ai: bool, output: str | None, fmt: str) -> int:
    module = get_module(name)
    data = module.analyzer(read_text(path))
    if ai:
        rendered = json.dumps(data, ensure_ascii=False) if isinstance(data, (dict, list)) else str(data)
        return run_ask(module.ai_prompt + "\n\n" + rendered)
    emit(name, path, data, output, fmt)
    return 0


def show_modules() -> int:
    for module in list_modules():
        print(f"{module.name:12} {module.description}")
    return 0


def run_workspace_new(name: str, root: str) -> int:
    print(f"Workspace created: {create_workspace(name, root)}")
    return 0


def run_workspace_status(path: str) -> int:
    print(json.dumps(workspace_status(path), indent=2))
    return 0


def run_chat() -> int:
    settings = load_settings()
    history = [{"role": "system", "content": settings.system_prompt}]
    print(f"CyberAI-Lab | provider={settings.provider} | model={settings.model}")
    print("Type /exit to quit or /clear to reset the conversation.")
    while True:
        try:
            prompt = input("\nYou> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not prompt:
            continue
        if prompt.lower() in {"/exit", "/quit"}:
            return 0
        if prompt.lower() == "/clear":
            history = [{"role": "system", "content": settings.system_prompt}]
            print("Conversation cleared.")
            continue
        history.append({"role": "user", "content": prompt})
        try:
            answer = complete(settings, history)
        except ProviderError as exc:
            history.pop()
            print(f"Error: {exc}")
            continue
        history.append({"role": "assistant", "content": answer})
        print(f"\nAI> {answer}")


def show_config() -> int:
    settings = load_settings()
    print(f"provider: {settings.provider}")
    print(f"model: {settings.model}")
    print(f"base_url: {settings.base_url}")
    print(f"timeout: {settings.timeout}")
    print(f"api_key_configured: {'yes' if settings.api_key else 'no'}")
    return 0


def report_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--ai", action="store_true", help="Optionally ask the configured AI provider to review parsed output.")
    parser.add_argument("--output", help="Write a report to this path.")
    parser.add_argument("--format", choices=("json", "md"), default="json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cyberai", description="Extensible AI-assisted CLI for authorized cybersecurity research.")
    sub = parser.add_subparsers(dest="command", required=True)

    ask = sub.add_parser("ask"); ask.add_argument("prompt")
    analyze = sub.add_parser("analyze"); analyze.add_argument("path")

    module = sub.add_parser("module", help="Run or inspect analyzer modules.")
    modules = module.add_subparsers(dest="module_command", required=True)
    modules.add_parser("list", help="List installed analyzer modules.")
    run = modules.add_parser("run", help="Run an analyzer module against a saved local file.")
    run.add_argument("name")
    run.add_argument("path")
    report_args(run)

    # Compatibility shortcuts retained from v0.2/v0.3.
    for name in ("http", "recon"):
        shortcut = sub.add_parser(name, help=f"Shortcut for: module run {name}")
        shortcut.add_argument("path")
        report_args(shortcut)

    workspace = sub.add_parser("workspace")
    ws = workspace.add_subparsers(dest="workspace_command", required=True)
    new = ws.add_parser("new"); new.add_argument("name"); new.add_argument("--root", default="workspaces")
    status = ws.add_parser("status"); status.add_argument("path")

    sub.add_parser("chat")
    sub.add_parser("config")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "ask":
            return run_ask(args.prompt)
        if args.command == "analyze":
            return run_analyze(args.path)
        if args.command == "module" and args.module_command == "list":
            return show_modules()
        if args.command == "module" and args.module_command == "run":
            return run_module(args.name, args.path, args.ai, args.output, args.format)
        if args.command in {"http", "recon"}:
            return run_module(args.command, args.path, args.ai, args.output, args.format)
        if args.command == "workspace" and args.workspace_command == "new":
            return run_workspace_new(args.name, args.root)
        if args.command == "workspace" and args.workspace_command == "status":
            return run_workspace_status(args.path)
        if args.command == "chat":
            return run_chat()
        if args.command == "config":
            return show_config()
    except (ValueError, ProviderError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
