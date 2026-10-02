from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_settings
from .providers import ProviderError, complete


def messages_for(prompt: str, system_prompt: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]


def run_ask(prompt: str) -> int:
    settings = load_settings()
    print(complete(settings, messages_for(prompt, settings.system_prompt)))
    return 0


def run_analyze(path: str) -> int:
    file_path = Path(path)
    if not file_path.is_file():
        raise ValueError(f"File not found: {file_path}")

    text = file_path.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        raise ValueError("The input file is empty.")

    prompt = (
        "Analyze the following text as authorized cybersecurity research material. "
        "Summarize what is directly supported by the evidence, identify notable "
        "security observations, separate facts from hypotheses, and suggest safe "
        "next validation steps.\n\n"
        f"--- INPUT ---\n{text}"
    )
    return run_ask(prompt)


def run_chat() -> int:
    settings = load_settings()
    history: list[dict[str, str]] = [
        {"role": "system", "content": settings.system_prompt}
    ]

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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cyberai",
        description="AI-assisted CLI for authorized cybersecurity research.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    ask = sub.add_parser("ask", help="Send a single prompt.")
    ask.add_argument("prompt")

    analyze = sub.add_parser("analyze", help="Analyze a local UTF-8 text file.")
    analyze.add_argument("path")

    sub.add_parser("chat", help="Start an interactive chat.")
    sub.add_parser("config", help="Show non-secret configuration.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "ask":
            return run_ask(args.prompt)
        if args.command == "analyze":
            return run_analyze(args.path)
        if args.command == "chat":
            return run_chat()
        if args.command == "config":
            return show_config()
    except (ValueError, ProviderError) as exc:
        parser.exit(1, f"Error: {exc}\n")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
