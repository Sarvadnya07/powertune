# ARCHITECTURE

## System Design
PowerTune is a layered Windows optimization platform with explicit separation between orchestration, telemetry, and mutable execution.

1. Entry layer: `cli/powertune.ps1` routes commands and enforces elevation checks for `-Apply`.
2. Telemetry layer: `core/telemetry.py` runs analyzers concurrently and merges plugin output.
3. Execution layer: `core/engine.py` parses YAML tweaks, applies firewall checks, and performs state changes.
4. Recovery layer: `rollback/snapshot.ps1` and `rollback/restore.ps1` capture and restore state.
5. Persistence layer: `core/database.py` stores events/metrics in SQLite under `reports/db`.

## Module Relationships
- Router -> Engine for profile operations (`battery`, `gaming`, `dev`, `silent`).
- Router -> Telemetry for diagnostics (`analyze`).
- Telemetry -> Analyzer modules + PluginManager.
- Engine -> rollback scripts + system command calls.
- Telemetry -> TelemetryDB for event persistence.

## Data Flow
1. User invokes command via PowerShell or Python entry point.
2. For analyze: analyzers emit JSON-style records (`category`, `severity`, `source`, `message`).
3. Records are merged, optional recommendations generated, then persisted.
4. For apply: profile is loaded, validated, snapshotted, executed tweak-by-tweak.
5. On failure during apply, restore script is invoked to roll back.

## Key Engineering Decisions
- Dry-run first: mutable operations require explicit `-Apply`.
- Intent firewall: critical services are blocked by default.
- Declarative profiles: easier review and contributor onboarding.
- Plugin discovery by convention (`get_telemetry`): low-friction extensibility.

## Known Gaps
- Profile signature verification currently returns `True` without strict hash enforcement.
- `cli/powertune.ps1` help includes `dashboard`, but ValidateSet does not currently list it.
- A subset of tests assert legacy `SystemExit` behavior instead of current exceptions.
