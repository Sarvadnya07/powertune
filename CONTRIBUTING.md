# Contributing to PowerTune

Thank you for your interest in contributing! Before writing any code, please read this document carefully — it defines the **non-negotiable principles** that every contribution must uphold.

---

## The Core Rule

> Every optimization PowerTune applies must be **explainable**, **reversible**, and **evidence-driven**.

If you cannot explain *why* a change improves battery life or performance with a concrete technical reason, it does not belong here.

---

## Before You Submit a PR

### For new optimization tweaks:
- [ ] You have a clear technical explanation for WHY this change works (link to docs, benchmarks, or source code if possible).
- [ ] The change is reversible. The profile script must call `snapshot.ps1` before applying.
- [ ] The change is gated behind the `-Apply` flag. Default execution is always dry-run.
- [ ] You have tested it on at least one real machine and documented the behavior.

### For new analyzer modules (`analyzers/*.py`):
- [ ] The analyzer outputs the standard contract: `status`, `message`, `why`, `recommendation`.
- [ ] You have written at least one unit test in `tests/` with mock data.
- [ ] The analyzer does **not** modify any system state — analyzers are read-only.

### For new vendor modules (`vendor/*.ps1`):
- [ ] The module auto-detects the vendor using WMI or service presence (not hardcoded).
- [ ] Service detection uses service names (not display names) for reliability.
- [ ] The module clearly marks which actions are destructive and requires the `-Apply` flag.

---

## What We Do NOT Accept

- Placebo tweaks (e.g., "clear RAM" scripts that just run `EmptyWorkingSet`)
- Tweaks that disable security features (e.g., Windows Defender, UAC)
- Permanent registry modifications without a documented and tested rollback path
- Scripts that require admin for diagnostic-only operations

---

## Development Setup

```powershell
# Clone and set up Python dependencies
git clone https://github.com/you/powertune
cd powertune
pip install beautifulsoup4 lxml

# Run the test suite
python -m pytest tests/ -v

# Run the analyzer (no admin needed)
.\cli\powertune.ps1 analyze
```

---

## Code Style

- **PowerShell**: Use `Write-Host` with color coding. `Cyan` = headers, `Yellow` = working, `Green` = success, `Red` = error, `Gray` = WHY explanations.
- **Python**: Follow PEP 8. Every public function must have a docstring. Use type hints.
- **Comments**: Prefer WHY comments over WHAT comments.

---

## Reporting Issues

When reporting a bug or unexpected behavior, please include:
1. Your laptop vendor and model
2. Output of `.\cli\powertune.ps1 analyze`
3. The full error message
4. Whether you ran with or without `-Apply`
