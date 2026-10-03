<p align="center"><img src="assets/cyberiq-logo.svg" width="86" alt="CyberIQ logo">&nbsp;&nbsp;<strong>CyberIQ</strong></p>

# CyberAI-Lab

## 👤 Developer & CyberIQ Leadership

**مقتدى الصدر جارالله خليف — Muqtada Al-Sadr Jarallah Khalif**  
**الحنتوشي — Al-Hantooshi**  
**Developer • Team Leader of CyberIQ**

CyberIQ focuses on cybersecurity, AI, networking, programming, CTF training, workshops, student projects, and practical labs.

---

A Python CLI for **AI-assisted cybersecurity research** in authorized labs, CTFs, education, and defensive security workflows.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-800020)
![Tests](https://img.shields.io/github/actions/workflow/status/hfsduu5-coder/CyberAI-Lab/tests.yml?label=tests)

> [!IMPORTANT]
> Only analyze systems, code, logs, or targets you own or have explicit permission to test.

## 📸 Preview

```text
CyberAI-Lab
├─ AI Providers     → Ollama / OpenAI-compatible
├─ Analyzer Modules → HTTP / Recon / Headers / Logs
├─ Workspaces       → Inputs / Reports / Notes
├─ Reporting        → JSON / Markdown / HTML
├─ Dashboard        → Local read-only HTML
└─ Diagnostics      → cyberai doctor
```

## v0.8 Highlights

- Interactive AI chat
- OpenAI-compatible API support
- Local Ollama support
- Generic text analysis
- **Offline HTTP request parser**
- **Offline reconnaissance-output summarizer**
- Optional AI interpretation of locally parsed results
- Input-size guard for local files
- Unit tests
- GitHub Actions test matrix for Python 3.10–3.12
- Dedicated security policy
- Local CTF/lab workspaces
- JSON, Markdown, and standalone HTML report export
- Contribution guide
- Module registry architecture with built-in `http`, `recon`, `headers`, and `logs` analyzers
- Installable Python package with a `cyberai` console command
- Offline response-header review module
- Offline log-summary module
- Safe demo inputs for immediate portfolio testing
- CI validation of package installation and CLI startup
- Read-only local HTML dashboard for workspaces and installed modules
- Dashboard works without a web server or extra dependency
- `cyberai doctor` local configuration diagnostics
- `cyberai --version` support
- End-to-end offline demo workflow in `examples/demo.py`
- Secrets kept outside source code through environment configuration

## Project Structure

```text
CyberAI-Lab/
├── .github/workflows/tests.yml
├── cyberai/
│   ├── __init__.py
│   ├── analyzers.py
│   ├── cli.py
│   ├── config.py
│   └── providers.py
├── tests/test_analyzers.py
├── .env.example
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── requirements.txt
└── README.md
```

## Installation

Requires Python 3.10+.

```bash
git clone https://github.com/hfsduu5-coder/CyberAI-Lab.git
cd CyberAI-Lab
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then:

```bash
pip install -r requirements.txt
cp .env.example .env
```

## Provider Configuration

### Ollama

```env
CYBERAI_PROVIDER=ollama
CYBERAI_MODEL=qwen2.5-coder
CYBERAI_BASE_URL=http://localhost:11434
```

### OpenAI-compatible endpoint

```env
CYBERAI_PROVIDER=openai
CYBERAI_MODEL=your-model
CYBERAI_API_KEY=your_key_here
CYBERAI_BASE_URL=https://api.openai.com/v1
```

Never commit a real API key.

## Commands

### Interactive chat

```bash
python -m cyberai.cli chat
```

### Single AI prompt

```bash
python -m cyberai.cli ask "Explain the difference between authentication and authorization"
```

### Analyze a text file with AI

```bash
python -m cyberai.cli analyze ./notes.txt
```

### Parse an HTTP request offline

Save an authorized/lab request to `request.txt`, then:

```bash
python -m cyberai.cli http request.txt
```

The parser reports request metadata such as method, host, path, parameter names, headers, content type, and body size. It does not contact the target.

Optionally send only the parsed report to your configured AI provider:

```bash
python -m cyberai.cli http request.txt --ai
```

### Summarize saved recon output offline

```bash
python -m cyberai.cli recon recon.txt
```

This extracts a small local summary from supplied text and **does not perform scanning**.

Optional AI review:

```bash
python -m cyberai.cli recon recon.txt --ai
```

### Show configuration

```bash
python -m cyberai.cli config
```

API keys are never printed.

## Modules

List built-in analyzer modules:

```bash
cyberai module list
```

Run a module against a saved local file:

```bash
cyberai module run http request.txt
cyberai module run recon recon.txt --output report.md --format md
cyberai module run headers examples/response-headers.txt
cyberai module run logs examples/app.log
cyberai module run headers examples/response-headers.txt --output report.html --format html
```

The older `cyberai http` and `cyberai recon` commands remain available as compatibility shortcuts.

## Quick Health Check

```bash
cyberai --version
cyberai doctor
```

The doctor checks Python compatibility, local configuration, registered modules, and project setup without probing external targets.

## End-to-End Demo

After `pip install -e .`, run:

```bash
python examples/demo.py
```

The demo exercises the CLI, offline analyzers, report generation, and dashboard using the repository's safe example data.

## Local Dashboard

Generate a read-only dashboard from your local workspaces:

```bash
cyberai dashboard
```

Or choose the workspace root and output file:

```bash
cyberai dashboard --root workspaces --output cyberai-dashboard.html
```

Open the generated HTML file in your browser. The dashboard is static and local: it does not start a server, scan targets, or upload workspace data.

## Workspaces & Report Export

Create an isolated local workspace for a lab or CTF:

```bash
python -m cyberai.cli workspace new demo-lab
python -m cyberai.cli workspace status workspaces/demo-lab
```

Export offline parser results as JSON, Markdown, or a portable HTML report:

```bash
python -m cyberai.cli http request.txt --output workspaces/demo-lab/reports/http.json --format json
python -m cyberai.cli recon recon.txt --output workspaces/demo-lab/reports/recon.md --format md
cyberai module run headers examples/response-headers.txt --output workspaces/demo-lab/reports/headers.html --format html
```

Workspaces are local organization helpers; they do not contact or scan targets.

## Tests

```bash
python -m unittest discover -s tests -v
```

GitHub Actions installs the package, runs the test suite on Python 3.10–3.13, and verifies the CLI entry point.

## Design Principles

1. **Authorization first** — designed for owned, lab, CTF, educational, and explicitly scoped environments.
2. **Evidence before claims** — analysis prompts distinguish observed facts from hypotheses.
3. **Local parsing first** — HTTP/recon parsers work offline; AI use is optional.
4. **Secrets stay out of Git** — credentials belong in local environment configuration.
5. **Small, auditable core** — keep the code understandable while the project grows.

## Roadmap

- Structured defensive analysis templates
- Additional safe local parsers
- Additional analyzer modules and extension points
- Richer structured report templates
- Provider adapters
- Local context/knowledge support
- Expanded tests and packaging

## Security

See [SECURITY.md](SECURITY.md). Never commit `.env`, credentials, tokens, private assessment data, or confidential target information.

## License

MIT.
