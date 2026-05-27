# PERFORMANCE

This document explains the performance posture of PowerTune itself (not only the optimizations it applies).

## What PowerTune Optimizes Internally
- Analyzer concurrency: telemetry collection runs multiple analyzers in parallel using `ThreadPoolExecutor` (`core/telemetry.py`).
- Bounded execution: subprocess calls use timeouts to avoid indefinite hangs.
- Local persistence: SQLite history prevents repeated “start from zero” investigations for recurring issues.

## Primary Costs
- Analyzer startup overhead (Python imports, subprocess calls).
- Per-tweak subprocess calls in apply mode (`powercfg`, `Stop-Service`, etc.).
- Plugin import and execution cost (unbounded without a budget today).

## Known Bottlenecks
- Large plugin sets can inflate telemetry runtime.
- High-frequency ingestion would stress SQLite; current usage is best-effort event logging.

## Scaling Strategy
- Add plugin execution budgets and scheduling (max runtime, max concurrency).
- Batch system queries where possible (reduce repeated shell calls).
- Introduce optional external sinks for fleet scenarios while keeping local-first behavior.

## Operator Best Practices
- Capture a baseline: run `analyze` and record the output.
- Run benchmarks before and after profile changes (where supported).
- Prefer small, explainable profile deltas over “mega profiles”.

