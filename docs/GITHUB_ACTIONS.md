# GitHub Actions Guide

## Active Workflows
- `ci.yml`: Windows matrix test/lint pipeline.
- `lint.yml`: focused linting and PowerShell analyzer checks.

## Current Gaps
- No release workflow for tags and packaged artifacts.
- No test artifact retention (benchmark reports, telemetry logs).

## Recommended Additions
- `release.yml` to build binaries and publish GitHub Release assets on version tags.
- Required status checks on `main` for both CI workflows.
- Scheduled workflow for dependency and script hygiene checks.
