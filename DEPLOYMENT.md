# DEPLOYMENT

## Deployment Model
PowerTune is endpoint software for Windows systems, not a hosted backend service.

## Production Rollout Steps
1. Validate code quality via CI (`ruff`, tests, PowerShell analyzer).
2. Package dependencies or binaries (`build.ps1` optional).
3. Roll out in dry-run mode first.
4. Enable controlled `-Apply` usage for approved operators.
5. Capture telemetry and rollback confidence before broad rollout.

## Environment Setup
- Ensure Python + PowerShell versions match documented baseline.
- Pre-create restore strategy and snapshot retention policy.

## CI/CD Recommendations
- Keep dual workflows for lint and test gates.
- Add release workflow for tags and packaged artifacts.
- Gate merges on passing safety tests.

## Hosting Suggestions
- Source hosting: GitHub.
- Artifact hosting: GitHub Releases for packaged binaries.
- Optional telemetry archive: central share or object storage for fleet analytics.

## Rollback Plan
- Every apply path should create snapshots under `rollback/snapshots`.
- Document operator procedure for emergency restore.
- Periodically test restore flow on representative hardware.
