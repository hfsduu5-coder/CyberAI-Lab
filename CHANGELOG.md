## 1.0.1
- Validate IPv4 observations before counting them in offline analyzers.
- Added regression coverage for malformed IPv4-like values.

# Changelog

All notable changes to CyberAI-Lab are documented here.

## [1.0.1] - 2026-10-03

First stable portfolio release.

### Added
- Modular offline analyzers for HTTP requests, reconnaissance text, response headers, logs, URLs, and indicator-like patterns.
- Optional Ollama and OpenAI-compatible AI providers.
- Local workspaces for inputs, reports, and notes.
- JSON, Markdown, and standalone HTML reports.
- Read-only local HTML dashboard.
- `cyberai doctor` diagnostics and `--version`.
- Safe example data and end-to-end demo workflow.
- Unit tests and GitHub Actions matrix for Python 3.10–3.13.
- Security and contribution documentation.

### Safety
- Offline analyzers do not scan or contact targets.
- Security workflows are documented for owned, lab, CTF, educational, defensive, or explicitly authorized environments.

## [0.9.0]
- Added offline URL inventory and indicator-pattern summary modules.

## [0.8.0]
- Added environment diagnostics, version command, and end-to-end demo.

## [0.7.0]
- Added read-only local dashboard generation.

## [0.6.0]
- Added standalone HTML report export.

## [0.5.0]
- Added response-header and log-summary modules plus safe examples.

## [0.4.0]
- Added module registry architecture and installable CLI package.

## [0.3.0]
- Added local workspaces and structured report export.

## [0.2.0]
- Added offline HTTP and recon analysis with tests and CI.

## [0.1.0]
- Initial CLI with Ollama and OpenAI-compatible provider support.
