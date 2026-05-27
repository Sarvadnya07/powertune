# CONTRIBUTING

PowerTune is safety-first. Changes that mutate system state require evidence and rollback validation.

## Contribution Workflow
1. Fork and branch from `main`.
2. Implement focused, reviewable changes.
3. Run lint and tests locally.
4. Open a PR using the template and include evidence.

## What to Contribute
- New analyzers under `analyzers/` (read-only telemetry modules).
- New profiles under `profiles/` (YAML DSL preferred).
- Safety improvements in `core/engine.py` and rollback scripts.
- Documentation and reproducible studies under `docs/` and `examples/`.

## Coding Standards
- Python: keep logic testable; use clear error types; avoid “catch-all and ignore” unless the caller expects it.
- PowerShell: strict mode compatible; predictable output; explicit elevation checks for mutation.
- Profiles: every tweak must include `risk` and `why`.

## Pull Request Requirements
- Rationale: explain the mechanism (OS-level reason) not just the expected outcome.
- Evidence: provide benchmark or measurable telemetry deltas for any new tuning behavior.
- Rollback: demonstrate snapshot + restore correctness for changes that mutate system state.
- Safety: denylist and validation rules must not regress.

## Branch Strategy (Suggested)
- `main`: stable integration branch
- `feature/*`: new analyzers and features
- `fix/*`: bug fixes
- `docs/*`: documentation-only changes

## Running Local Checks
```powershell
pytest -q
ruff check .
```

