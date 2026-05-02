name: Feature Request / New Analyzer
about: Suggest a new optimization profile or diagnostic telemetry analyzer.
title: "[FEATURE] "
labels: enhancement
assignees: ''

---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. "I have a Dell XPS and `DellOptimizer.exe` is waking the CPU constantly."

**Describe the solution you'd like**
A clear and concise description of what you want to happen. Are you proposing a new YAML profile or a new Python analyzer for `core/telemetry.py`?

**Describe the scientific rationale (Mandatory)**
Per our contributing guidelines, please explain the OS-level mechanism. Why does this improve power efficiency or latency?
> Example: "Disabling XYZ service prevents the WMI provider from polling the EC every 1ms, allowing the CPU package to enter the C8 sleep state."

**Pre-and-Post Benchmark Evidence (Mandatory for Tweaks)**
Provide data showing the impact.
- Idle Power Before: X.X Watts
- Idle Power After: Y.Y Watts

**Additional context**
Add any other context or screenshots about the feature request here.
