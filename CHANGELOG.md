# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-02
### Added
- **Core DSL Engine**: YAML-based declarative optimization engine (`core/engine.py`).
- **Intent Firewall**: Hardcoded security sandbox blocking modifications to critical Windows services.
- **Atomic Rollbacks**: Automatic snapshot generation and restoration on execution failures.
- **Deep Diagnostics**: Python analyzers for Battery wear, CPU states, GPU residency, and Service Dependencies.
- **Vendor Intelligence**: Detection modules for ASUS, Lenovo, Dell, and HP bloatware.
- **Safety Policy**: 50-point constitution strictly forbidding placebo tweaks and destructive actions.
- **Diagnostic Bundler**: Zips reports for easy GitHub issue generation.

### Security
- Patched YAML command injection vulnerability in `ServiceDisable` tweaks.
- Added strict `check=True` to all subprocesses to prevent silent `powercfg` execution failures.
