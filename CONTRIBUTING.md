# Contributing to PowerTune

Thank you for contributing to PowerTune. We follow a standard GitHub Flow model.

## Development Workflow
1. **Fork and Branch:** Create a focused feature branch from `main`:
   ```bash
   git checkout -b feature/analyzer-name
   ```
2. **Implement Changes:** Keep changes atomic and conceptually focused.
3. **Local Validation:**
   ```powershell
   # Run unit tests
   pytest -q

   # Run Python lint check
   ruff check .

   # Verify PowerShell scripts
   Invoke-ScriptAnalyzer -Path . -Recurse | Where-Object { $_.Severity -eq 'Error' }
   ```
4. **Open a Pull Request:** Submit your PR against `main`. Complete the PR checklist and provide rationale or before/after benchmark numbers where applicable.

## Coding Standards
- **Python:** Formatted and linted using `ruff`. Follow PEP 8 style conventions.
- **PowerShell:** Follow PowerShell standard scripting guidelines; pass PSScriptAnalyzer with zero Errors.
- **Commit Messages:** Use imperative, descriptive commit subjects (e.g., `feat: add timer resolution analyzer` or `fix: handle missing battery report`).
- **Safety Policy:** Any state-altering tweak must implement dry-run capability, Intent Firewall checks, and atomic snapshot/restore support.

