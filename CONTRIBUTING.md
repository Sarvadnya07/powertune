# Contributing to the PowerTune Ecosystem

Welcome to PowerTune. This project has evolved from a simple script collection into an **Elite-Level Systems Observability and Power Intelligence Platform**. 

Because we operate in a space plagued by "placebo optimizers" and dangerous registry hacks, we enforce an extremely strict engineering culture. If you are submitting code or configuration profiles here, you are agreeing to these standards.

---

## 🛑 1. The Zero-Placebo Rule
PowerTune operates purely on **Evidence-Driven Optimization**. 
- We do NOT accept "RAM Cleaners", "TCP Network Boosters", or "Gaming Mode Registry Spams".
- Every single profile tweak must have a measurable, scientific impact. If you cannot prove it reduces WMI battery drain rates, decreases CPU package power, or resolves DPC latency, your PR will be rejected.

---

## 🧩 2. YAML Declarative Profiles (No Spaghetti PowerShell)
Do not submit raw `.ps1` or `.bat` files for system tweaks.
All optimizations must be submitted as **Declarative YAML Profiles** (`profiles/*.yaml`). 

Your YAML tweak must include:
1. `id`: Must map to an existing handler in `engine.py`.
2. `risk`: Must be classified (Low, Medium, High, Critical).
3. `why`: A mandatory, human-readable rationale that will be displayed in the CLI to educate the user.

---

## 🛡️ 3. Mandatory Rollback & Reversibility
We operate on a **Transaction-Based Optimization Model**. 
- If you add a new tweak handler to `core/engine.py`, you **MUST** ensure that `rollback/snapshot.ps1` and `rollback/restore.ps1` are updated to capture and restore the state of whatever subsystem you are touching.
- Permanent, irreversible changes to the OS are strictly forbidden.

---

## 📊 4. Telemetry Standard
If you are submitting a new analyzer (e.g., `analyzers/memory_pressure.py`), it must integrate with our **Unified Telemetry Schema**.
- Do not just `print()` outputs.
- Your analyzer must support the `--json` flag and output an array of telemetry objects containing: `category`, `severity`, `source`, and `message`.
- This ensures your data can be consumed by the automated AI Recommendation Engine (`core/telemetry.py`).

---

## 🧪 5. Submitting a Pull Request

When you open a PR, your description must include the following **Validation Matrix**:

1. **Rationale**: Technical explanation of OS-level behavior being changed.
2. **Benchmark Data**: Pre-and-post `core/benchmark.py` data (e.g., "Idle drain dropped from 12W to 8W").
3. **Rollback Proof**: Proof that running `restore.ps1` returns the system identically to its prior state.

### PR Checklist
- [ ] Added `timeout=` arguments to all new subprocess calls.
- [ ] Enforced `check=True` on state-mutating subprocesses to guarantee Atomic Rollbacks.
- [ ] Passed the Intent Firewall (did not touch critical blocklisted services).
- [ ] Passed the GitHub Actions CI pipeline (`flake8` and `PSScriptAnalyzer`).

---

We are building the definitive enterprise-grade power observability platform for Windows. Thank you for holding the line on engineering quality!
