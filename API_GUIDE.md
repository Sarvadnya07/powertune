# API_GUIDE

PowerTune is a CLI toolchain (PowerShell + Python). This guide documents internal APIs for contributors.

## Engine API
### `execute_profile(yaml_path, apply_changes=False, root_dir='.')`
- Location: `core/engine.py`
- Purpose: transaction-style profile execution.
- Workflow: validate -> snapshot (if apply) -> apply tweaks -> verify -> commit.
- Exceptions:
  - `ProfileNotFoundError`
  - `EngineInitializationError`
  - `SecurityViolationError`
  - `PowerTuneError`

### Tweak registry
`TWEAK_REGISTRY` maps tweak IDs to executable classes:
- `cpu_min_state`
- `cpu_max_state`
- `active_scheme`
- `service_disable`

## Telemetry API
### `collect_telemetry(root_dir='.')`
- Location: `core/telemetry.py`
- Behavior:
  - runs analyzer scripts concurrently
  - merges plugin results from `plugins/`
  - persists events via `TelemetryDB` when available

### `generate_recommendations(telemetry, root_dir='.')`
- Location: `core/telemetry.py`
- Behavior:
  - renders rich console output if UI deps are available
  - emits heuristic recommendations for high severity and GPU residency patterns
  - attempts predictive hooks from `core/predictions.py`

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

Recommended plugin behavior:
- fast and side-effect free (telemetry only)
- does not require admin rights for read-only diagnostics
- fails closed: catches internal exceptions and returns `[]` rather than crash the pipeline

## CLI Contract
Primary router: `cli/powertune.ps1`
- analyze
- benchmark
- battery
- gaming
- dev
- silent
- vendor
- restore
- help

Note: `dashboard` is implemented in the script but currently not included in the command ValidateSet.

## “API-like” usage examples
Telemetry pipeline (developer usage):
```powershell
python -c "from core.telemetry import collect_telemetry; print(len(collect_telemetry('.')))"
```

Profile engine:
```powershell
python core/engine.py profiles/battery.yaml --root .
python core/engine.py profiles/battery.yaml --root . --apply
```

