from __future__ import annotations
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

def read_text(path: str, max_bytes: int = 1_000_000) -> str:
    p=Path(path)
    if not p.is_file(): raise ValueError(f"File not found: {p}")
    if p.stat().st_size>max_bytes: raise ValueError(f"Input exceeds the {max_bytes:,}-byte safety limit.")
    text=p.read_text(encoding="utf-8",errors="replace")
    if not text.strip(): raise ValueError("The input file is empty.")
    return text

def parse_http_request(raw: str) -> dict:
    lines=raw.replace("\r\n","\n").split("\n")
    if not lines or not lines[0].strip(): raise ValueError("No HTTP request line found.")
    parts=lines[0].split()
    if len(parts)!=3 or not parts[2].startswith("HTTP/"): raise ValueError("Expected request line: METHOD PATH HTTP/x.x")
    method,target,version=parts
    headers={}; body_start=len(lines)
    for i,line in enumerate(lines[1:],start=1):
        if line=="": body_start=i+1; break
        if ":" in line:
            k,v=line.split(":",1); headers[k.strip()]=v.strip()
    body="\n".join(lines[body_start:]); parsed=urlsplit(target)
    query_keys=sorted({x.split("=",1)[0] for x in parsed.query.split("&") if x})
    return {"method":method.upper(),"path":parsed.path or "/","version":version,
        "host":next((v for k,v in headers.items() if k.lower()=="host"),""),
        "query_parameter_names":query_keys,"header_names":sorted(headers),
        "content_type":next((v for k,v in headers.items() if k.lower()=="content-type"),""),
        "body_bytes":len(body.encode("utf-8"))}

def http_report(raw: str) -> str:
    return json.dumps(parse_http_request(raw),indent=2,ensure_ascii=False)

def recon_report(text: str) -> str:
    urls=re.findall(r"https?://[^\s\]\[<>'\"]+",text)
    ips=re.findall(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])",text)
    codes=re.findall(r"(?<!\d)([1-5]\d{2})(?!\d)",text)
    hosts=[urlsplit(u).hostname.lower() for u in urls if urlsplit(u).hostname]
    lines=["Recon Summary","=============",f"Lines: {len(text.splitlines())}",f"URLs found: {len(urls)}",f"Unique URL hosts: {len(set(hosts))}",f"IPv4-like values: {len(set(ips))}"]
    if hosts: lines+=["\nTop hosts:"]+[f"- {h}: {n}" for h,n in Counter(hosts).most_common(10)]
    if codes: lines+=["\nObserved HTTP-like status codes:"]+[f"- {c}: {n}" for c,n in Counter(codes).most_common()]
    lines.append("\nNote: This parser summarizes supplied text only; it does not scan or contact targets.")
    return "\n".join(lines)

def headers_report(text: str) -> dict:
    headers={}
    for line in text.replace("\r\n","\n").split("\n"):
        if ":" in line:
            k,v=line.split(":",1); headers[k.strip().lower()]=v.strip()
    checks={
        "content-security-policy":"Helps constrain browser content sources.",
        "strict-transport-security":"Requests HTTPS-only behavior after a secure visit.",
        "x-content-type-options":"Helps prevent MIME-type sniffing.",
        "referrer-policy":"Controls referrer information sent by the browser.",
        "permissions-policy":"Controls access to selected browser capabilities.",
    }
    return {"present_security_headers":sorted(k for k in checks if k in headers),
            "missing_security_headers":sorted(k for k in checks if k not in headers),
            "observed_header_names":sorted(headers),
            "note":"Missing headers are review signals, not proof of a vulnerability."}

def log_summary(text: str) -> dict:
    lines=[x for x in text.splitlines() if x.strip()]
    levels=Counter()
    for line in lines:
        for level in ("ERROR","WARN","WARNING","INFO","DEBUG","CRITICAL"):
            if re.search(rf"\b{level}\b",line,re.I):
                levels[level.upper()]+=1; break
    ipv4=set(re.findall(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])",text))
    return {"lines":len(lines),"level_counts":dict(sorted(levels.items())),"unique_ipv4_like_values":len(ipv4),
            "note":"Offline summary only; values are not validated or contacted."}
