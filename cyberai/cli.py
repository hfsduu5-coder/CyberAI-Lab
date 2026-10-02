from __future__ import annotations

import argparse
from pathlib import Path

from .analyzers import http_report, read_text, recon_report
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
    text = read_text(path)
    prompt = (
        "Analyze the following text as authorized cybersecurity research material. "
        "Summarize what is directly supported by the evidence, identify notable "
        "security observations, separate facts from hypotheses, and suggest safe "
        "next validation steps.\n\n"
        f"--- INPUT ---\n{text}"
    )
    return run_ask(prompt)


def run_http(path: str, ai: bool) -> int:
    raw = read_text(path)
    report = http_report(raw)
    if not ai:
        print(report)
        return 0
    prompt = (
        "Review this HTTP request metadata from an authorized lab. Explain the "
        "request structure, identify security-relevant observations supported by "
        "the metadata, and suggest safe validation questions. Do not invent a "
        "vulnerability.\n\n"
        f"{report}"
    )
    return run_ask(prompt)


def run_recon(path: str, ai: bool) -> int:
    text = read_text(path)
    report = recon_report(text)
    if not ai:
        print(report)
        return 0
    prompt = (
        "Review this offline summary of user-supplied reconnaissance output. "
        "Prioritize observations, distinguish evidence from hypotheses, and suggest "
        "authorized next validation steps.\n\n"
        f"{report}"
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

    analyze = sub.add_parser("analyze", help="Analyze a local UTF-8 text file with AI.")
    analyze.add_argument("path")

    http = sub.add_parser("http", help="Parse an HTTP request file offline.")
    http.add_argument("path")
    http.add_argument("--ai", action="store_true", help="Send parsed metadata to the configured AI provider.")

    recon = sub.add_parser("recon", help="Summarize saved reconnaissance output offline.")
    recon.add_argument("path")
    recon.add_argument("--ai", action="store_true", help="Send the offline summary to the configured AI provider.")

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
        if args.command == "http":
            return run_http(args.path, args.ai)
        if args.command == "recon":
            return run_recon(args.path, args.ai)
        if args.command == "chat":
            return run_chat()
        if args.command == "config":
            return show_config()
    except (ValueError, ProviderError) as exc:
        parser.exit(1, f"Error: {exc}\n")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
