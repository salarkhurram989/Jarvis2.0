# JARVIS 2.0

A separate Windows desktop companion for the JARVIS project.

JARVIS 2.0 uses the **existing JARVIS Gemini backend** for general AI conversations, so you do **not** need to paste your Gemini API key into this desktop app.

## PC capabilities

- AI conversations through the existing JARVIS API
- Search accessible Windows drives for files
- Open matching files
- Find and launch applications from common Windows Start Menu/Desktop locations
- Open explicit file/folder paths
- Dark JARVIS-style desktop interface

## Setup

### Easiest option

Download the **JARVIS-Setup.exe** installer produced by GitHub Actions. It installs JARVIS 2.0, creates Start Menu and Desktop shortcuts, and can launch JARVIS immediately after installation.

The installer is self-contained: the target PC does not need Python or Node.js installed.

### Direct installer download

**JARVIS 2.0 Windows Installer:**  
https://productionresultssa1.blob.core.windows.net/actions-results/fe929051-c2fc-4e56-9d3e-365e571acc86/workflow-job-run-a39e11e9-31ad-5ecb-bf7a-ea98a7753597/artifacts/c1752a8e3e60907cdfb0dbf8ab45f93a736aad908ea50bd982fd66b63fc9fbaa.zip?rscd=attachment%3B+filename%3D%22JARVIS2-Windows-Installer.zip%22&rsct=application%2Fzip&se=2026-09-29T11%3A48%3A50Z&sig=ZLOMbkD%2B%2B61BrCS5udPGZMfF33Q7CtvBUdlFkzXvcFY%3D&ske=2026-09-29T14%3A10%3A43Z&skoid=ca7593d4-ee42-46cd-af88-8b886a2f84eb&sks=b&skt=2026-09-29T10%3A10%3A43Z&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skv=2025-11-05&sp=r&spr=https&sr=b&st=2026-09-29T11%3A38%3A45Z&sv=2025-11-05

> **Note:** This is a temporary GitHub Actions artifact link and will expire. For a permanent download, use the GitHub Actions artifact from the latest successful Windows build.

### Run from source

Install Python 3.11+ and run:

```
python jarvis_pc.py
```

No third-party Python packages are required.

## Example commands

- `find my PDFs`
- `search for report`
- `open Chrome`
- `open C:\\Games\\game.exe`
- `What is the capital of France?`

## Security

The desktop app only performs its built-in file search/open-app/open-file actions. It does not expose arbitrary Windows shell commands.

The Gemini API key stays on the original JARVIS backend and is not included in this repository.

> Keep API credentials private. Google recommends using environment variables or server-side secret storage and never committing API keys to source control. See Google's Gemini API key guidance.
