# CyberAI-Lab

A Python CLI for **AI-assisted cybersecurity research** in authorized labs, CTFs, education, and defensive security workflows.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-800020)
![Tests](https://img.shields.io/github/actions/workflow/status/hfsduu5-coder/CyberAI-Lab/tests.yml?label=tests)

> [!IMPORTANT]
> Only analyze systems, code, logs, or targets you own or have explicit permission to test.

## v0.2 Highlights

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

## Tests

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs the test suite on Python 3.10, 3.11, and 3.12.

## Design Principles

1. **Authorization first** — designed for owned, lab, CTF, educational, and explicitly scoped environments.
2. **Evidence before claims** — analysis prompts distinguish observed facts from hypotheses.
3. **Local parsing first** — HTTP/recon parsers work offline; AI use is optional.
4. **Secrets stay out of Git** — credentials belong in local environment configuration.
5. **Small, auditable core** — keep the code understandable while the project grows.

## Roadmap

- Structured defensive analysis templates
- Additional safe local parsers
- Report export
- Provider adapters
- Local context/knowledge support
- Expanded tests and packaging

## Security

See [SECURITY.md](SECURITY.md). Never commit `.env`, credentials, tokens, private assessment data, or confidential target information.

## License

MIT.
