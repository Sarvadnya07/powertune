# Release Workflow

## Branch to Release Flow
1. Merge validated work into `main`.
2. Bump version in `pyproject.toml`.
3. Update `CHANGELOG.md` with dated release notes.
4. Tag release: `vX.Y.Z`.
5. CI builds artifacts and publishes GitHub release.

## Release Quality Gates
- Lint passes.
- Tests pass (or known exceptions documented and approved).
- Security-sensitive changes reviewed.
- Rollback path verified for mutable operations.

## SemVer Policy
- MAJOR: breaking CLI/profile behavior changes.
- MINOR: backward-compatible features and analyzers.
- PATCH: fixes, docs, and safe maintenance updates.
