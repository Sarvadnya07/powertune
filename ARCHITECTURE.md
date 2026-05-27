# ARCHITECTURE

## System Design
PowerTune is a layered Windows optimization platform with explicit separation between orchestration (PowerShell), telemetry (Python analyzers), and mutable execution (profile engine + rollback).

1. Entry layer: `cli/powertune.ps1` routes commands and enforces elevation checks for `-Apply`.
2. Telemetry layer: `core/telemetry.py` runs analyzers concurrently and merges plugin output.
3. Execution layer: `core/engine.py` parses YAML tweaks, enforces the intent firewall, and performs system changes.
4. Recovery layer: `rollback/snapshot.ps1` and `rollback/restore.ps1` capture and restore state.
5. Persistence layer: `core/database.py` stores events/metrics in SQLite under `reports/db`.

## Module Relationships
- Router -> Engine for profile operations (`battery`, `gaming`, `dev`, `silent`).
- Router -> Telemetry for diagnostics (`analyze`).
- Telemetry -> Analyzer modules + PluginManager.
- Engine -> rollback scripts + system command calls.
- Telemetry -> TelemetryDB for event persistence.

## Data Flow
1. User runs a command via PowerShell or Python entrypoint.
2. For `analyze`: analyzers emit event records and optional recommendations are rendered.
3. Events are persisted to local history (SQLite).
4. For profile apply: YAML is parsed -> validated -> snapshotted -> applied tweak-by-tweak.
5. On apply failure: restore script reverts captured state.

## Key Engineering Decisions
- Dry-run first: mutable operations require explicit `-Apply`.
- Intent firewall: critical services are blocked by default; service names are validated.
- Declarative profiles: reviewable, diffable, and easier to audit than imperative scripts.
- Plugin discovery by convention (`get_telemetry`): low-friction extensibility for OEM/custom telemetry.

## Stability Contracts
### Telemetry event schema
Analyzers and plugins should emit a list of objects shaped like:
```json
{"category":"gpu","severity":"high","source":"chrome.exe","message":"dGPU residency detected during idle"}
```

### Profile execution contract
- Apply mode snapshots before mutation.
- Safety violations surface as typed exceptions (engine) and are presented to operators (router).
- Unknown tweak IDs are currently warnings; a strict mode would upgrade to errors for managed environments.

## Known Gaps (as of 2026-05-27)
- Profile signature verification returns `True` without strict hash enforcement.
- `cli/powertune.ps1` implements `dashboard`, but `ValidateSet` does not list it.
- A subset of tests assert legacy `SystemExit` behavior rather than current typed exceptions.

