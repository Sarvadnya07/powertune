# OPEN_SOURCE_IMPROVEMENT_PLAN

## Already Present in Repo
- CI workflows: `.github/workflows/ci.yml`, `.github/workflows/lint.yml`
- Issue templates: `.github/ISSUE_TEMPLATE/*` plus `.github/ISSUE_TEMPLATE/config.yml`
- PR template: `.github/PULL_REQUEST_TEMPLATE.md`
- Community docs: `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`
- Release and actions docs: `docs/RELEASE_WORKFLOW.md`, `docs/GITHUB_ACTIONS.md`

## High-ROI Improvements (Recommended Next)
1. Release workflow automation
   - Add `.github/workflows/release.yml` to build artifacts and publish GitHub Releases on tag push.
2. Explicit support matrix
   - Document tested Windows versions, Python versions, PowerShell versions, and “requires admin” surface.
3. “Safety policy as code”
   - Move critical firewall rules into a documented policy file and add CI tests that ensure the rules cannot regress.
4. Snapshot retention + UX
   - Add commands to list snapshots, prune by age/count, and verify restore integrity.
5. Docs IA cleanup
   - Add `docs/INDEX.md` as the canonical documentation entrypoint and keep filenames stable.

## Contributor Experience
- Add `CODEOWNERS` for core areas (engine, analyzers, PowerShell router).
- Add “PR types” guidance: analyzer additions vs profile changes vs safety changes.
- Add benchmark artifact requirements for profile changes (attach before/after evidence).

