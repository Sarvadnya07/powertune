# SECURITY

PowerTune can modify system state. This document describes the security posture and the controls that reduce risk.

## Security Architecture
- Operator boundary: `cli/powertune.ps1` is the primary interface and enforces admin checks for `-Apply`.
- Execution boundary: `core/engine.py` implements the tweak registry and the intent firewall.
- Recovery boundary: rollback scripts snapshot and restore state (`rollback/snapshot.ps1`, `rollback/restore.ps1`).

## Core Controls (Current Implementation)
- Dry-run by default.
- `-Apply` requires local admin elevation.
- Service-name input validation (regex) before any service operations.
- Critical service denylist (`CRITICAL_SERVICES_BLOCKLIST` in `core/engine.py`).
- Snapshot-before-change in apply mode; restore path available via `restore`.

## Data Handling
- No secrets are required to run PowerTune.
- Logs and telemetry are local by default:
  - `reports/changes.log` (JSONL)
  - `reports/db/telemetry_history.db` (SQLite)

## Threat Model (Practical)
- Malicious or unsafe profiles attempting to disable security services.
- Command injection via tweak parameters (especially service names).
- Partial application leaving the machine in an inconsistent state.

## Hardening Roadmap
- Strict profile signing (hash allowlist) with a managed “strict mode”.
- Schema validation for profile YAML (required keys, allowed tweak IDs, value ranges).
- Policy allowlists by environment (workstation vs managed endpoint).
- CI tests that ensure denylist coverage cannot regress.

## Reporting Vulnerabilities
Prefer private disclosure via GitHub Security Advisories. Include:
- affected version/commit
- reproduction steps
- commands and profile used
- expected vs observed behavior
- rollback outcome

