# CONTRIBUTING

## Contribution Workflow
1. Fork and branch from `main`.
2. Implement focused, reviewable changes.
3. Run lint + tests locally.
4. Submit PR with rationale and verification notes.

## Coding Standards
- Python: keep functions small, explicit, and testable.
- PowerShell: strict mode compatible, clear operator messages.
- Profiles: every tweak must include `risk` and `why`.
- Do not introduce optimizations without measurable evidence.

## Pull Request Guidelines
PRs should include:
- problem statement
- implementation summary
- risk impact
- validation outputs (`pytest`, analyzer checks, benchmark if relevant)
- rollback implications for mutable behavior

## Branch Strategy
- `main`: stable integration branch
- `feature/*`: isolated feature work
- `fix/*`: targeted bug fixes
- `docs/*`: documentation-only updates

## Review Expectations
- Security posture cannot regress.
- User safety and recoverability are first-class requirements.
- Claims about power/perf improvements must be reproducible.
