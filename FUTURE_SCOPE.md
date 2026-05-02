# 🚀 FUTURE SCOPE: PowerTune Roadmap

This document outlines the strategic vision and upcoming milestones for PowerTune, evolving it from a powerful CLI toolkit into an enterprise-grade systems engineering and observability platform.

---

## 🟢 Short-Term Improvements (Next Release)

1.  **Dependency Management**: Add a formal `requirements.txt` and `setup.py` for standard Python package distribution.
2.  **ETW Tracing (Event Tracing for Windows)**: Implement deep hooks into the Windows Scheduler via `pywintrace` to capture DPC latency spikes and identify exactly which processes interrupt connected standby (S0i3).
3.  **WMI Live Polling**: Introduce a daemon command to poll CPU package power (Watts) and thermal sensors in real-time, outputting JSON streams.
4.  **CLI UX Overhaul**: Integrate the `Rich` Python library to replace standard terminal outputs with gorgeous, styled tables, syntax-highlighted JSON, and progress bars.

---

## 🟡 Mid-Term Enhancements

1.  **Auto-Profile Daemon (Auto-Switcher)**:
    *   A lightweight, low-footprint background service that listens for system events.
    *   *Example*: Unplugging AC power automatically triggers the `battery.yaml` profile. Launching `Cyberpunk2077.exe` automatically applies `gaming.yaml`.
2.  **Benchmarking Engine**:
    *   Automated pre- and post-optimization measurement. 
    *   PowerTune will measure idle power draw for 60 seconds, apply the profile, measure again, and report the exact wattage delta.
3.  **Cross-Vendor Abstraction Layer**:
    *   Fully flesh out the Lenovo (Vantage), Dell (SupportAssist), and HP module stubs to actively pause telemetry logic dynamically across all hardware.

---

## 🔴 Long-Term Vision

1.  **Tauri / SvelteKit GUI Dashboard**:
    *   Transition from a purely CLI tool to a beautiful, dark-mode desktop application.
    *   Visual representation of the Service Dependency Graph.
    *   Live thermal timelines and pie-chart attribution of battery drain per process.
2.  **Cloud-Synced Profiles & Community Hub**:
    *   Allow users to share, rate, and download custom YAML profiles for specific laptop models directly through the application.

---

## 🔐 Security Upgrades

1.  **Cryptographic Signature Verification**:
    *   Ensure the DSL engine only executes `.yaml` files that match an approved cryptographic hash, preventing local tampering or supply-chain attacks.
2.  **Granular Privilege Escalation**:
    *   Instead of running the entire CLI as Administrator, use Just-In-Time (JIT) elevation only when invoking `powercfg` or stopping a service, keeping the analysis layer strictly unprivileged.

---

## ⚡ Performance Optimizations

1.  **Compiled Core Engine**:
    *   Compile the Python DSL parser (`engine.py`) using `Nuitka` or `PyInstaller` to remove the Python runtime dependency for end-users.
2.  **Asynchronous Analysis**:
    *   Refactor the `Invoke-Analyze` pipeline to run battery, CPU, GPU, and service analyzers concurrently using Python `asyncio`, dropping diagnostic generation time from ~3 seconds to under 500ms.

---

## 🤖 AI & Elite Analytics (Phase 21)

1.  **Rule-Based Recommendation Engine**: Analyze WMI telemetry and suggest profiles. (e.g., "Chrome is responsible for 37% of wakeups. Recommend Battery Profile.")
2.  **Predictive Hardware Aging**: Forecast thermal paste degradation and battery replacement timing based on historical voltage curves.
3.  **Adaptive Profiles**: Automatically switch between gaming, coding, and battery saver profiles based on active foreground processes.

---

## 🏢 Enterprise & Fleet Scale (Phase 22)

1.  **Fleet Diagnostics**: Centralized reporting dashboard for monitoring multiple enterprise devices.
2.  **Security Hardening**: Detect hidden crypto-miners, suspicious wakeup triggers, and malicious persistence mechanisms disguised as vendor bloatware.
3.  **Compliance Mode**: Strict, IT-approved optimization policies that lock specific registry edits.

---

## 📊 Elite-Level Differentiators (Phase 23)

1.  **Power-State Visualization**: GUI module to visualize CPU C-states, GPU residency, and exact sleep transitions (S0i3) over time.
2.  **Wakeup Graph Analysis**: Real-time graphs showing exactly which processes are waking the CPU out of deep idle.
3.  **DPC/ISR Latency Monitoring**: Track hard-interrupts causing audio crackling and gaming micro-stutters.

---

## 🌌 The Power Intelligence Ecosystem (Phases 25-38 Epics)

As PowerTune matures from a diagnostics toolkit into a full **Systems Observability Platform**, the following enterprise-grade epics will be developed:

*   **Event Correlation Engine**: Automatically cross-reference CPU spikes, GPU wakeups, and battery drain events to generate root-cause analysis (e.g., "Battery drain increased by 4W explicitly because Chrome requested a 1ms timer").
*   **Time-Series Telemetry DB**: Transition from JSON logs to a local time-series database tracking thermal saturation, fan curve efficiency, and hardware aging curves over years of use.
*   **Security & Forensics Crossover**: Implement real-time heuristics to detect crypto-miners (abnormal idle power draw) and stealth persistence mechanisms disguised as vendor telemetry.
*   **Fleet Analytics**: Remote diagnostics and enterprise compliance modes for company-wide laptop efficiency monitoring.
*   **Cross-Platform Expansion**: Port the diagnostic telemetry engine to Linux (eBPF) and macOS to create the ultimate, universal power-intelligence framework.

---

## 🔄 DevOps / CI-CD Ideas

1.  **GitHub Actions Integration**:
    *   **Linting**: Enforce `flake8` and `black` on all Python files. Enforce `PSScriptAnalyzer` on all PowerShell code.
2.  **Automated Security Testing**:
    *   CI pipeline that runs `tests/test_security.py` to guarantee the Intent Sandbox blocklist is never accidentally removed by a pull request.
3.  **Automated Releases**:
    *   GitHub Actions workflow to package `powertune.ps1`, compile the Python binaries, and create versioned release bundles upon tagging.
