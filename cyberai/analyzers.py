from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit


def read_text(path: str, max_bytes: int = 1_000_000) -> str:
    file_path = Path(path)
    if not file_path.is_file():
        raise ValueError(f"File not found: {file_path}")
    if file_path.stat().st_size > max_bytes:
        raise ValueError(f"Input exceeds the {max_bytes:,}-byte safety limit.")
    text = file_path.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        raise ValueError("The input file is empty.")
    return text


def parse_http_request(raw: str) -> dict:
    lines = raw.replace("\r\n", "\n").split("\n")
    if not lines or not lines[0].strip():
        raise ValueError("No HTTP request line found.")

    parts = lines[0].split()
    if len(parts) != 3 or not parts[2].startswith("HTTP/"):
        raise ValueError("Expected request line: METHOD PATH HTTP/x.x")

    method, target, version = parts
    headers: dict[str, str] = {}
    body_start = len(lines)

    for index, line in enumerate(lines[1:], start=1):
        if line == "":
            body_start = index + 1
            break
        if ":" in line:
            name, value = line.split(":", 1)
            headers[name.strip()] = value.strip()

    body = "\n".join(lines[body_start:])
    parsed = urlsplit(target)
    query_keys = sorted({item.split("=", 1)[0] for item in parsed.query.split("&") if item})
    content_type = next(
        (value for name, value in headers.items() if name.lower() == "content-type"),
        "",
    )

    return {
        "method": method.upper(),
        "path": parsed.path or "/",
        "version": version,
        "host": next((v for k, v in headers.items() if k.lower() == "host"), ""),
        "query_parameter_names": query_keys,
        "header_names": sorted(headers),
        "content_type": content_type,
        "body_bytes": len(body.encode("utf-8")),
    }


def http_report(raw: str) -> str:
    info = parse_http_request(raw)
    return json.dumps(info, indent=2, ensure_ascii=False)


def recon_report(text: str) -> str:
    urls = re.findall(r"https?://[^\s\]\[<>'\"]+", text)
    ips = re.findall(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])", text)
    status_codes = re.findall(r"(?<!\d)([1-5]\d{2})(?!\d)", text)

    hosts = []
    for url in urls:
        host = urlsplit(url).hostname
        if host:
            hosts.append(host.lower())

    lines = [
        "Recon Summary",
        "=============",
        f"Lines: {len(text.splitlines())}",
        f"URLs found: {len(urls)}",
        f"Unique URL hosts: {len(set(hosts))}",
        f"IPv4-like values: {len(set(ips))}",
    ]

    if hosts:
        lines.append("\nTop hosts:")
        lines.extend(f"- {host}: {count}" for host, count in Counter(hosts).most_common(10))
    if status_codes:
        lines.append("\nObserved HTTP-like status codes:")
        lines.extend(f"- {code}: {count}" for code, count in Counter(status_codes).most_common())

    lines.append("\nNote: This parser summarizes supplied text only; it does not scan or contact targets.")
    return "\n".join(lines)
