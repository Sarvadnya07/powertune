## Pull Request Overview
Briefly describe the purpose of this PR. Does it add a new analyzer, fix a bug, or introduce a new YAML optimization profile?

## Mandatory Validation Checklist
Because PowerTune enforces a Zero-Placebo policy, all PRs that modify the system state must be mathematically validated.

- [ ] **Rationale Provided**: I have explained exactly *why* this change improves system observability or efficiency.
- [ ] **Benchmark Data Attached**: If adding an optimization, I have run `core/benchmark.py` and provided the before/after idle drain data below.
- [ ] **Rollback Tested**: I have manually verified that `snapshot.ps1` and `restore.ps1` correctly revert my changes.
- [ ] **No Security Downgrades**: This PR does not disable Windows Defender, UAC, or critical updates.
- [ ] **Telemetry Compliance**: If adding an analyzer, it supports the `--json` flag and standard schema.

## Benchmark Data
```text
(Paste pre-and-post watt drain or latency metrics here)
```

## Related Issues
Fixes # (issue number)
