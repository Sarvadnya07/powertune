# Changelog

All notable changes to the PowerTune ecosystem will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-02
### Added
- **Core Engine API**: Introduced `core/engine.py` utilizing the Command Pattern for transactional, safe system optimizations.
- **Intent Firewall**: Hardcoded `CRITICAL_SERVICES_BLOCKLIST` to prevent malicious shutdown of Windows Defender, RPC, and critical updates.
- **Atomic Rollbacks**: Integrated hexadecimal WMI state capture into `rollback/snapshot.ps1` with `check=True` subprocess safety.
- **Unified Telemetry Schema**: Built `core/telemetry.py` to aggregate JSON analytics streams.
- **Interactive Web Dashboard**: Added `core/dashboard.py` to compile stateless, dark-mode `Chart.js` telemetry visualizations.
- **Diagnostics Suite**: 
  - `gpu_residency.py` (dGPU P-State tracking)
  - `sleep_states.py` (S0ix Modern Standby wake triggers)
  - `timers.py` (Platform Timer Resolution abuse)
  - `thermal.py` (ACPI Thermal Zone saturation)
  - `power_attribution.py` (Process-level battery estimation)
  - `anomaly.py` (Crypto-miner / runaway background CPU detection)
- **Vendor Abstraction**: Added hardware-aware modules for ASUS, Lenovo, Dell, and HP.
- **CI/CD Pipeline**: GitHub Actions workflow (`flake8`, `PSScriptAnalyzer`) for automated security testing.
- **Portable Binaries**: Added `build.ps1` for PyInstaller compilation of standalone executables.

### Changed
- Migrated all configuration from hardcoded PowerShell scripts to declarative, typed YAML profiles (`profiles/battery.yaml`, `profiles/gaming.yaml`).
- Enforced the **Zero-Placebo Rule** requiring WMI wattage benchmarks for all community pull requests.

### Removed
- Removed legacy, unvalidated "registry spam" scripts.
- Removed dangerous placebo tweaks (e.g., "RAM cleaners").
