# Security Policy

## Reporting a Vulnerability
If you discover a security vulnerability in PowerTune, please report it responsibly:
1. **GitHub Security Advisory (Recommended):** Submit a report at [Security Advisories](https://github.com/Sarvadnya07/powertune/security/advisories/new).
2. **Direct Contact:** Email the maintainer at `sarvadnyasonkambale0@gmail.com` with subject prefix `[SECURITY]`.

Please include:
- Affected version/commit
- Proof of concept or reproduction steps
- Assessment of impact (e.g. elevation of privilege, arbitrary script execution)

We acknowledge reports within 48 hours and will coordinate a patch before public disclosure.

## Security Architecture
- **No Remote Execution:** PowerTune intentionally lacks a network listener by default to eliminate RCE vectors.
- **Privilege Separation:** UI processes run as standard users; only the core data collection engine requests elevation for hardware control.
- **Intent Firewall:** Optimizations validate service and registry modifications against `docs/SAFETY_POLICY.md` before applying changes.
- **Verification:** Unit tests in `tests/test_security.py` validate sandbox boundary enforcement.

## Handling Sensitivities
We actively strip out personally identifiable information (PII) such as personal file paths and user SIDs from ETW traces before local storage or analysis.

