# PowerTune Testing Guide

This document outlines the validation procedures for PowerTune to ensure system safety and diagnostic accuracy.

## 🧪 Automated Testing (CI/CD)
PowerTune uses `pytest` for Python core validation and `PSScriptAnalyzer` for PowerShell linting. These run automatically on every GitHub Push/PR.

### Running Local Tests
```powershell
# Run the Python test suite
pytest tests/

# Run the PowerShell linter
Invoke-ScriptAnalyzer -Path . -Recurse
```

## 🛠️ Manual Validation Matrix
For every new optimization profile, the following manual checks must be performed:

| Check | Procedure | Expected Result |
| :--- | :--- | :--- |
| **Dry-Run Mode** | Run `.\cli\powertune.ps1 <profile>` | No system changes occur; `changes.log` shows 'Dry-Run'. |
| **Apply Mode** | Run `.\cli\powertune.ps1 <profile> -Apply` | Registry/Services are modified; Snapshot is created in `reports/`. |
| **Atomic Rollback**| Run `.\cli\powertune.ps1 restore -Apply` | System state returns to 100% identical pre-optimization state. |
| **Telemetry Accuracy**| Run `.\cli\powertune.ps1 dashboard` | JSON data matches manual `Get-Service` and `powercfg` queries. |

## 🛡️ Security Sanity Checks
1.  **Blocklist Verification**: Attempt to create a YAML profile that disables `windefend`. The engine must throw an immediate `Intent Firewall` exception.
2.  **Unprivileged Access**: Verify that `.\cli\powertune.ps1 analyze` works perfectly without Administrator rights (Read-only mode).
3.  **Command Injection**: Attempt to pass `target: "svc; rm -rf /"` in a YAML profile. The regex validator must catch and reject the string.

---
*Maintained by the PowerTune Engineering Team*
