# SECURITY

## Security Architecture
PowerTune uses defensive defaults to reduce system risk during optimization.

## Core Controls
- Dry-run default for all profile operations.
- Explicit elevation required for mutable `-Apply` operations.
- Critical service blocklist in engine (`CRITICAL_SERVICES_BLOCKLIST`).
- Service target regex validation before execution.
- Snapshot-before-change rollback model.

## Sensitive Configuration Handling
- No secrets are required for core runtime.
- Telemetry and change logs are local files under `reports/`.
- Contributors should avoid storing machine-identifying details in committed artifacts.

## Threat Considerations
- Malicious profile attempts to disable core services.
- Command injection via service-name payloads.
- Incomplete rollback under partial-apply failure.

## Hardening Recommendations
- Enforce strict profile signature checks.
- Add profile schema validation and policy allowlists.
- Add CI tests for blocklist behavior and rollback integrity.
- Add static analysis for PowerShell scripts in mandatory CI gate.

## Responsible Disclosure
Report security issues privately before public disclosure. Provide:
- reproduction steps
- affected commands/profiles
- observed/expected behavior
- mitigation suggestions if available
