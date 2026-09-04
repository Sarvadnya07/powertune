# SETUP_GUIDE

This guide gets PowerTune running on Windows and covers the common failure modes (Python, execution policy, elevation).

## Prerequisites
- Windows 10/11
- Python 3.10+
- PowerShell 5.1+
- Administrator privileges for any command that uses `-Apply`

## Quick Setup (Recommended)
```powershell
git clone https://github.com/Sarvadnya07/powertune.git
cd powertune
.\install.ps1
```

What `install.ps1` does:
- creates `.venv` if missing
- installs Python dependencies from `requirements.txt`
- optionally adds `<repo>\cli` to your User `PATH`

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

Expected local outputs/artifacts:
- change log: `reports/changes.log` (JSONL)
- telemetry history: `reports/db/telemetry_history.db` (SQLite)
- snapshots (apply mode): `rollback/snapshots/*.json`

## Troubleshooting
### “Python not found”
- Validate: `python --version`
- Fix: install Python 3.10+ and ensure it is on PATH, or use `install.ps1` to configure `.venv`.

### “Running scripts is disabled”
- PowerTune uses `-ExecutionPolicy Bypass` for routed commands, but your environment may still block script execution.
- Workaround for a single command:
```powershell
powershell.exe -ExecutionPolicy Bypass -File .\cli\powertune.ps1 analyze
```

### “-Apply requires Administrator”
- Start a PowerShell terminal as Administrator, then re-run the command with `-Apply`.

### Analyzer failures
- Most analyzers are read-only. If one fails, the telemetry pipeline is designed to continue with partial results.
- Ensure dependencies are installed: `pip install -r requirements.txt`

