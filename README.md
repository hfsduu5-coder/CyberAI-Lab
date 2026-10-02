# CyberAI-Lab

A lightweight Python CLI for experimenting with AI-assisted cybersecurity workflows in **authorized labs, CTFs, education, and security research**.

> [!IMPORTANT]
> CyberAI-Lab is an educational/research project. Only analyze systems, code, logs, or targets you own or have explicit permission to test.

## Why this project?

Security work often involves repetitive analysis: reviewing HTTP traffic, understanding findings, summarizing reconnaissance output, and turning raw notes into clear next steps. CyberAI-Lab provides a small provider-agnostic CLI foundation for those workflows without hard-coding credentials into the project.

## Features

- Interactive terminal chat
- OpenAI-compatible API support
- Local Ollama support
- Configurable model, endpoint, timeout, and system prompt
- Analyze local text files from the command line
- No API keys stored in source code
- Minimal dependencies and simple architecture
- Designed for extension with defensive/security research workflows

## Project Structure

```text
CyberAI-Lab/
├── cyberai/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   └── providers.py
├── .env.example
├── .gitignore
├── LICENSE
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

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy the example environment file:

```bash
cp .env.example .env
```

Windows:

```powershell
Copy-Item .env.example .env
```

## Providers

### Ollama (local)

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

The CLI uses the standard OpenAI-compatible `/chat/completions` interface.

## Usage

Interactive mode:

```bash
python -m cyberai.cli chat
```

Single prompt:

```bash
python -m cyberai.cli ask "Explain the security impact of this finding"
```

Analyze a local text file:

```bash
python -m cyberai.cli analyze ./notes.txt
```

Show non-secret configuration:

```bash
python -m cyberai.cli config
```

## Roadmap

- Structured security-analysis templates
- Safer parsing of reconnaissance output
- Report-generation workflows
- Additional provider adapters
- Optional local knowledge/context support
- Tests and CI

## Security

Never commit `.env`, API keys, tokens, credentials, private target data, or confidential assessment output.

## License

MIT License.
