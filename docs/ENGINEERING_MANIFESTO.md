# The PowerTune Engineering Manifesto

This document outlines the non-negotiable engineering core of the PowerTune project. If these fundamentals are upheld, the project remains an elite, professional-grade platform. If they are ignored, the project devolves into a random collection of scripts.

---

## 🧠 1. Systems Thinking (Most Important)
We do not "run tweaks blindly." We think in dependencies, side effects, observability, and reproducibility. The platform is designed to understand the OS state *before* and *after* any modification.

## 🛡️ 2. Absolute Safety Engineering
Every optimization must be **reversible, validated, scoped, and logged**.
- **Must Have**: Rollbacks, granular hex snapshots, restore points, and compatibility checks.
- **Must NEVER Happen**: Bricking Windows, disabling critical services (RPC, Defender), or unsafe registry deletions.

## 🔭 3. Observability First
This is the true foundation. Before optimizing, we measure, analyze, and attribute causes.
Our core observability domains: CPU usage, wakeups, timer resolution, battery drain, GPU residency, thermal behavior, and S0ix sleep states.

## 🔬 4. Evidence-Driven Engineering
Every single tweak must answer two questions:
1. **WHY does this help?** (OS-level rationale)
2. **HOW MUCH does it help?** (Measured wattage/latency delta)

## 🏗️ 5. Clean Architecture & Modularity
The architecture must be modular, layered, and extensible.
- **The Pipeline**: `CLI -> Core Engine -> Telemetry Analyzer -> Optimizer API -> OS Interface`
- Every subsystem (battery, gpu, thermal, vendor, rollback) is strictly isolated.

## ⏪ 6. Guaranteed Rollback System
Professional tools always support rollback. PowerTune can undo changes, restore precise power plans, and revert targeted services using the `rollback/restore.ps1` atomic transaction system.

## 🩺 7. Diagnostics & Root-Cause Analysis
Diagnostics are the heart of the project. We do not stop at symptoms ("System slow" or "Battery draining"). We identify the root cause ("Chrome requested 1ms timer resolution, preventing CPU C8 residency").

## 📊 8. Unified Telemetry Design
Telemetry must be structured, timestamped, categorized, and normalized. Our JSON pipeline guarantees that AI recommendations and dashboards can consume the data uniformly.

## 📚 9. Core Domain Knowledge
Maintainers must deeply understand:
- **Windows Internals**: Services, WMI, ETW, powercfg, DWM, svchost.
- **Power Management**: CPU C-states, P-states, ASPM, Connected Standby, USB selective suspend.
- **Hardware Awareness**: AMD vs Intel variance, iGPU vs dGPU routing, and vendor-specific firmware behavior.

## 🔌 10. Vendor Abstraction
ASUS ≠ Lenovo ≠ Dell. Vendor-specific logic is strictly contained within isolated `vendor/` modules, ensuring safe execution across different hardware boundaries.

## ⚙️ 11. Configuration Design
Profiles (`battery.yaml`, `gaming.yaml`) are typed, validated, and versioned. Hardcoded magic values in execution scripts are banned.

## 🧪 12. Benchmarking Science & Testing
We measure before and after applying changes. We evaluate repeatability and variance using `core/benchmark.py`. We explicitly test rollback failures and unsupported systems.

## 🤝 13. User Trust & Explainability
Trust is everything. We never hide actions, obfuscate behavior, or apply silent tweaks. Every action explains what changed, why it changed, the expected impact, and how to revert it.

## 🔒 14. Security Model
The Intent Firewall (`CRITICAL_SERVICES_BLOCKLIST`) protects the host from dangerous commands, malicious plugins, and unsafe community scripts.

## 💻 15. Professional Tooling
- **CLI Design**: Clean, structured verbs (`powertune analyze`, `powertune battery`).
- **Logging**: Atomic `changes.log` capturing timestamps, actions, and risk severity.
- **Documentation**: Comprehensive architecture, rationale, and usage guides.

---

## 🎯 The Final Core Truth

PowerTune is **NOT** an "optimization script."
PowerTune is a **Systems Observability and Controlled Optimization Platform.**

We prioritize safety, clarity, evidence, and maintainability over hype and placebo claims. This discipline is what makes the project engineering-grade.
