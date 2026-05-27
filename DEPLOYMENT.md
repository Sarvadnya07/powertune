# DEPLOYMENT

PowerTune is endpoint software for Windows systems. It is not a hosted backend service.

## Deployment Modes
- Developer workstation: install via `install.ps1` and run locally.
- Operator-managed endpoint: staged rollout using dry-run first, then controlled `-Apply`.
- Portable binaries (optional): `build.ps1` compiles selected Python entrypoints using PyInstaller.

## Production Rollout Steps
1. Validate build quality via CI (lint + tests).
2. Run `analyze` on representative hardware and capture baseline telemetry artifacts.
3. Apply profiles only under operator policy with snapshot verification.
4. Validate restoration workflow periodically using recent snapshots.
5. Collect and store artifacts for audit:
   - `reports/changes.log`
   - `reports/db/telemetry_history.db`
   - `rollback/snapshots/*.json`

## CI/CD Recommendations
- Require both workflows to pass:
  - `.github/workflows/ci.yml`
  - `.github/workflows/lint.yml`
- Add a release workflow that publishes binaries on tag push.
- Upload benchmark/telemetry artifacts as CI artifacts for PR review.

## Hosting Suggestions
- Source: GitHub.
- Artifacts: GitHub Releases (signed, versioned).
- Optional telemetry archive: central share or object storage for fleet analytics.

