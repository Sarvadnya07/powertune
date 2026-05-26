# SETUP_GUIDE

## Prerequisites
- Windows 10/11
- Python 3.10+
- PowerShell 5.1+
- Administrator access for `-Apply` commands

## Quick Setup
```powershell
git clone https://github.com/Sarvadnya07/powertune.git
cd powertune
.\install.ps1
```

## Manual Setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Verify Installation
```powershell
.\cli\powertune.ps1 help
.\cli\powertune.ps1 analyze
pytest -q
```

## Troubleshooting
- Python not found: install Python and verify `python --version`.
- Script policy errors: run with explicit `-ExecutionPolicy Bypass`.
- Non-admin apply failure: run terminal as Administrator.
- Missing analyzer deps: re-run `pip install -r requirements.txt` in `.venv`.

## Optional PATH Setup
Add `<repo>\\cli` to User PATH to call `powertune.ps1` without full path.
