# 🔋 PowerTune

> **Safe, explainable, modular, and reversible laptop optimization & diagnostics for Windows.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://www.microsoft.com/windows)
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1%2B-blue)](https://github.com/PowerShell/PowerShell)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Security: Sandboxed](https://img.shields.io/badge/Security-Sandboxed-brightgreen.svg)](docs/SAFETY_POLICY.md)

---

## 📖 Overview

Most "optimizer" scripts found online are either fundamentally unsafe, rely on placebo tweaks, or silently corrupt the Windows registry. **PowerTune** is an engineering-grade system optimization and diagnostic toolkit. 

Instead of blindly applying generic tweaks, PowerTune **diagnoses first**, **explains every action**, and **strictly enforces reversibility**. Powered by a YAML-based Domain Specific Language (DSL) and a robust Intent Firewall, PowerTune allows power users, developers, and gamers to extract maximum performance and battery life safely.

---

## ✨ Core Features

*   **🛡️ Intent Firewall**: Hardcoded blocklists prevent any YAML profile from disabling critical security services (e.g., Windows Defender, UAC, DHCP).
*   **📊 Deep Diagnostics**: Python-powered analyzers parse `powercfg` reports, query WMI, and poll `nvidia-smi` to identify exactly what is preventing deep sleep.
*   **⚙️ DSL Configuration**: Profiles are entirely declarative (YAML), eliminating messy monolithic scripts.
*   **♻️ Snapshot & Rollback**: Every applied profile automatically captures the current system state, allowing instant, perfect rollbacks.
*   **🕸️ Dependency Graphing**: Automatically maps parent-child dependencies of vendor bloatware (like ASUS Armoury Crate) before taking action.
*   **📦 Portable Bundles**: One-click generation of sanitized diagnostic `.zip` bundles for issue reporting.

---

## 📸 Demo / Screenshots

*(Placeholder for future dashboard and CLI execution recordings)*

```text
> .\cli\powertune.ps1 analyze

  🔹 Diagnostic Analyzer
     [*] Detected vendor: ASUS
         WHY: Vendor detection tailors diagnostic checks to known bloat services.
     
     [*] Running GPU analyzer...
     [!] WARNING: dGPU is active. 
         - Discord.exe
         WHY: When the dGPU is active, system power draw increases by 10-20W even at idle.
```

---

## 🛠️ Tech Stack

*   **Core Execution**: `PowerShell 5.1+` (System interop, WMI, Process control)
*   **DSL Engine & Analyzers**: `Python 3.8+` (Data parsing, YAML processing, WMI Graphing)
*   **Dependencies**: `PyYAML`, `BeautifulSoup4`, `lxml`

---

## 🏗️ Architecture

1.  **CLI Dispatcher**: (`powertune.ps1`) Handles user input, vendor detection, and routing.
2.  **Analyzers**: Python modules that run read-only queries against system performance metrics and hardware states.
3.  **DSL Engine**: (`engine.py`) Parses YAML profiles, evaluates risk scores, triggers the rollback snapshot, and translates declarations into `powercfg` / Win32 commands.
4.  **Intent Sandbox**: Validates all targets against `CRITICAL_SERVICES_BLOCKLIST`.

---

## 🚀 Installation

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/yourusername/powertune.git
   cd powertune
   ```
2. **Install Python requirements:**
   ```powershell
   pip install -r requirements.txt
   ```
   *(Note: Ensure Python is added to your system PATH)*

---

## 💻 Usage Instructions

**Run Diagnostics (No Admin Required):**
```powershell
.\cli\powertune.ps1 analyze
```

**Dry-Run a Profile (Safe Preview):**
```powershell
.\cli\powertune.ps1 battery
```

**Apply a Profile (Requires Admin):**
```powershell
.\cli\powertune.ps1 battery -Apply
```

**Restore Previous State:**
```powershell
.\cli\powertune.ps1 restore -Apply
```

**Generate Diagnostic Bundle:**
```powershell
python cli\powertune_bundle.py
```

---

## ⚙️ Configuration

Profiles are defined in `profiles/*.yaml`. Example structure:
```yaml
profile: battery
description: Maximize idle efficiency
tweaks:
  - id: cpu_min_state
    value: 5
    risk: Low
    why: "Allows CPU to enter deeper C-states."
```

---

## 📂 Folder Structure

```text
powertune/
├── analyzers/             # Python diagnostic engines (CPU, GPU, Battery, Dependencies)
├── cli/                   # PowerShell dispatcher and launcher
├── core/                  # engine.py (DSL Parser and Security Sandbox)
├── docs/                  # Architecture & SAFETY_POLICY.md
├── profiles/              # YAML optimization profiles
├── reports/               # Generated WMI/Battery outputs
├── rollback/              # State saving & restoration logic
├── tests/                 # Unit tests (test_security.py, test_parsers.py)
└── vendor/                # OEM-specific bloat detection scripts
```

---

## ⚡ Performance / Optimization Notes

PowerTune does not run persistent background agents (Phase 1). It is an on-demand configuration manager. Running an analysis or applying a profile consumes negligible resources and leaves zero lingering processes.

---

## 🔒 Security Considerations

PowerTune operates strictly under the [50-Rule Safety & Ethics Policy](docs/SAFETY_POLICY.md).
- **No Remote Payloads**: PowerTune never downloads executable code.
- **Sandboxing**: `engine.py` will hard-halt if a YAML profile targets critical OS infrastructure.
- **Rollback Guarantee**: Destructive changes are banned. State mutation is explicitly tracked.

---

## 🤝 Contributing Guidelines

We welcome contributions! However, all pull requests must strictly adhere to our [Safety Policy](docs/SAFETY_POLICY.md). 
- Every new tweak must include a verifiable `why` explanation.
- No placebo tweaks (e.g., RAM cleaners).
- Include tests for any new parser logic.

---

## 📄 License

MIT License — Copyright (c) 2026 PowerTune Contributors. See `LICENSE` for details.
