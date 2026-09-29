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
