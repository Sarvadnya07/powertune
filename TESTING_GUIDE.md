# TESTING_GUIDE

Testing in PowerTune prioritizes safety and correctness of behavior under both dry-run and apply flows.

## Test Layers
- Unit tests: parser/format handling and pure logic where possible.
- Safety tests: intent firewall behavior, YAML parsing stability, dry-run non-destructiveness.
- Regression checks: telemetry persistence behavior and restore logic assumptions.

## Run Tests
```powershell
pytest -q
```

## Current Status (2026-05-27)
- Local result: 7 passed, 2 failed.
- Failures are expectation mismatches:
  - `tests/test_engine.py` expects `SystemExit`, engine raises `SecurityViolationError`.
  - `tests/test_security.py` expects `SystemExit`, engine raises `SecurityViolationError`.

This is documented in `README.md` so contributors are not surprised by CI behavior.

## Manual Testing Runbook
Read-only diagnostics:
```powershell
.\cli\powertune.ps1 analyze
```

Dry-run profile:
```powershell
.\cli\powertune.ps1 battery
```

Apply profile (Administrator):
```powershell
.\cli\powertune.ps1 battery -Apply
```

Restore (Administrator):
```powershell
.\cli\powertune.ps1 restore -Apply
```

## Edge Cases Worth Automating Next
- malformed YAML and unknown tweak IDs
- blocked critical services and injection-like service names
- plugin import failures (must not crash the pipeline)
- snapshot selection and restore when no snapshots exist

