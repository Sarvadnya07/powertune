# FUTURE_SCOPE

## Short-Term (0-3 months)
- Align failing security tests with current exception contract (`SecurityViolationError`).
- Add schema validation for profile YAML.
- Add dashboard assets/screenshots and report export presets.
- Add deterministic benchmark harness for before/after profile comparison.

## Mid-Term (3-9 months)
- Signed profile manifests with strict hash enforcement.
- Policy engine for allow/deny tweak classes by environment (personal/workstation/lab).
- Fleet mode for applying profile policy across multiple Windows endpoints.
- Richer anomaly correlation across CPU, timer, and wake-source events.

## Long-Term (9-18 months)
- Multi-platform abstraction layer for Linux parity (already hinted in docs).
- Optional remote telemetry sink (OTLP/Timeseries DB).
- Recommendation ranking with confidence scores and automated experiment loops.

## Scalability Evolution
- Move from local SQLite to pluggable persistence adapters.
- Add analyzer job queue and controlled concurrency for large plugin sets.
- Add release-channel config (stable/canary) for profiles and analyzers.

## AI / Automation Opportunities
- Automated root-cause graph generation from telemetry events.
- Drift detection between expected and observed power-state outcomes.
- CI bot comments that validate optimization claims against benchmark artifacts.

## DevOps Evolution
- Signed releases and supply-chain attestation.
- Automated versioning + release notes generation.
- Matrix testing across more Windows editions and hardware classes.
