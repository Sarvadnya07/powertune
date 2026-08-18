## System Design
PowerTune utilizes a **Hub-and-Spoke** architecture decoupled via a standardized JSON telemetry contract.
- **The Engine (core/engine.py):** Acts as the central orchestrator, managing the lifecycle of plugins and analyzers.
- **Data Persistence (core/database.py):** Local SQLite storage optimized for time-series writes (WAL mode enabled).

## Data Flow
1. **Polling/Tracing:** nalyzers/ consume WMI classes and ETW traces asynchronously.
2. **Normalization:** Data is scrubbed, typed, and normalized into a standard JSON schema in core/telemetry.py.
3. **Analysis:** core/intelligence.py cross-references metrics against historical baselines to flag anomalies (e.g., unexpected timer resolution changes).
4. **Action/Storage:** Output is presented to the UI/CLI and persisted to SQLite.

## Key Engineering Decisions
- **Why SQLite over JSON files?** For concurrent read/writes during high-frequency telemetry polling (100ms intervals).
- **Why PowerShell for Rollback?** To ensure maximum OS-level compatibility and leverage native Windows APIs for registry/service restoration without external dependencies.
