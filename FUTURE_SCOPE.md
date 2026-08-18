## Short-Term Improvements
- **Expanded Hardware Plugins:** Deeper integration with AMD Ryzen Master API and Intel XTU for micro-voltage telemetry.
- **Tauri Dashboard Enhancements:** Adding historical time-series graphs (via SQLite) directly into the UI.

## Long-Term Roadmap
- **Linux Port (See docs/linux_port_architecture.md):** Translating ETW paradigms to eBPF/perf events for cross-platform data center deployments.
- **Fleet Management:** Cloud-synchronized telemetry for enterprise IT departments to manage hardware efficiency across thousands of endpoints.

## AI & Automation
- **Predictive Thermal Throttling:** Utilizing a lightweight ML model (XGBoost/LightGBM) trained on local telemetry to pre-emptively adjust power limits before thermal saturation occurs.
