# API_GUIDE

## Scope
PowerTune is a CLI toolchain. This guide documents internal programmatic APIs for contributors.

## Engine API
### `execute_profile(yaml_path, apply_changes=False, root_dir='.')`
- Location: `core/engine.py`
- Purpose: transaction-style profile execution.
- Steps: validate -> snapshot (if apply) -> apply tweaks -> verify -> commit.
- Exceptions:
  - `ProfileNotFoundError`
  - `EngineInitializationError`
  - `SecurityViolationError`
  - `PowerTuneError`

### Tweak Registry
`TWEAK_REGISTRY` maps tweak IDs to executable classes:
- `cpu_min_state`
- `cpu_max_state`
- `active_scheme`
- `service_disable`

## Telemetry API
### `collect_telemetry(root_dir='.')`
- Location: `core/telemetry.py`
- Behavior:
  - runs selected analyzer scripts concurrently
  - merges plugin results from `plugins/`
  - persists events via `TelemetryDB`

### `generate_recommendations(telemetry, root_dir='.')`
- Behavior:
  - renders rich console output if UI deps available
  - emits heuristics for high severity and GPU residency issues
  - tries predictive hooks from `core/predictions.py`

## Plugin API
### Plugin contract
A plugin module must expose:
```python
def get_telemetry() -> list[dict]:
    ...
```
Expected event shape:
```json
{"category":"gpu","severity":"high","source":"plugin_name","message":"..."}
```

## CLI Contract
Primary command router: `cli/powertune.ps1`
- analyze
- benchmark
- battery
- gaming
- dev
- silent
- vendor
- restore
- help

## Error Handling
- Engine raises typed exceptions for policy violations and malformed inputs.
- PowerShell router catches fatal errors and directs users to logs.
