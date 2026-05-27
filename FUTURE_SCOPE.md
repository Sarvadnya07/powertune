# FUTURE_SCOPE

This document is an engineering roadmap. It prioritizes safety, measurability, and maintainability over “more tweaks”.

## Short-Term (0-3 months)
- Align failing security tests with the engine contract (`SecurityViolationError` vs `SystemExit`) and codify the error semantics.
- Add YAML schema validation and required fields enforcement (`profile`, `tweaks[*].id`, `risk`, `why`).
- Fix `cli/powertune.ps1` command surface mismatch (`dashboard` is implemented but not in ValidateSet).
- Add snapshot retention policy and snapshot listing UX (`rollback/snapshots` can grow unbounded).
- Add `desktop/README.md` and a minimal telemetry mock adapter for UI iteration.

## Mid-Term (3-9 months)
- Signed profile manifests and strict hash enforcement (opt-in “strict mode” first, then default).
- Policy engine: allow/deny tweak classes by environment (personal workstation, corporate endpoint, lab).
- Expand analyzer contracts to enforce a stable event schema and versioning for plugin compatibility.
- Benchmark harness: baseline capture + apply + re-measure with artifact output for CI and PR review.

## Long-Term (9-18 months)
- Fleet operations model: profile distribution, audit logs, and rollbacks across multiple devices.
- Optional remote telemetry sink (OTLP or custom adapters) while keeping local-first mode.
- Correlation engine improvements: link timer abuse, wake sources, GPU residency, and drain deltas into a causal graph.

## Scalability Evolution
- Pluggable persistence: SQLite (local) -> adapter interface -> external TSDB (optional).
- Analyzer scheduling: concurrency budgets, timeouts, and cost heuristics for plugin sets.
- Release channels: stable/canary profile streams with “known-good” compatibility tags.

## AI / Automation Opportunities
- Automated root-cause narratives driven by event clusters (grounded in measured telemetry).
- Drift detection: “expected profile outcome” vs “observed outcome” with confidence and reasons.
- CI bots: validate optimization claims against benchmark artifacts, not prose.

## DevOps Evolution
- Signed releases, SBOM generation, and supply-chain attestations.
- Automated changelog + semantic versioning enforcement on tags.
- Expanded CI matrix: Windows editions, PowerShell versions, and minimal-permissions runs.

