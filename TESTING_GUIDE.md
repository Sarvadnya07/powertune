# TESTING_GUIDE

## Test Strategy
PowerTune testing prioritizes safety and behavior correctness over synthetic coverage metrics.

## Test Layers
- Unit tests: parser and helper behavior.
- Safety tests: engine validation, firewall, and dry-run stability.
- Regression checks: profile execution paths and telemetry persistence.

## Run Tests
```powershell
pytest -q
```

## Current Observations (2026-05-27)
- Result: 7 passed, 2 failed.
- Failing files:
  - `tests/test_engine.py`
  - `tests/test_security.py`
- Root cause: tests assert `SystemExit` while engine now raises `SecurityViolationError`.

## Manual Testing
- `./cli/powertune.ps1 analyze`
- `./cli/powertune.ps1 battery`
- `./cli/powertune.ps1 battery -Apply` (admin)
- `./cli/powertune.ps1 restore -Apply` (admin)

## Edge Cases to Cover
- malformed YAML syntax
- unsupported tweak IDs
- blocked critical services
- plugin import/runtime failure
- restore behavior when snapshot list is empty

## Future Automation
- Add contract tests for plugin payload schema.
- Add integration tests that mock `powercfg` and service operations.
- Add CI artifact upload for benchmark and telemetry outputs.
