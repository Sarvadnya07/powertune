# Security Policy

## Supported Versions
PowerTune is a community-driven platform. We currently provide security updates for the following versions:

| Version | Supported |
| :--- | :--- |
| 1.0.x | ✅ Yes |
| < 1.0.0 | ❌ No |

## Reporting a Vulnerability
We take the security of your system seriously. If you discover a security vulnerability (e.g., a bypass of the Intent Firewall, a potential command injection, or a privilege escalation vector), please do not open a public Issue.

Instead, please send a detailed report to: **security@powertune.io** (Placeholder)

### What to include:
- A detailed description of the vulnerability.
- A proof-of-concept (PoC) script or set of steps to reproduce.
- The potential impact (e.g., "Allows disabling Windows Defender via modified YAML").

## Our Process
1.  **Acknowledgment**: We will acknowledge your report within 48 hours.
2.  **Investigation**: Our core team will validate the vulnerability.
3.  **Resolution**: We aim to provide a patch or mitigation within 10 business days.
4.  **Disclosure**: We will coordinate a public disclosure after the patch is released.

## The Intent Firewall
PowerTune utilizes an "Intent Firewall" to block the modification of critical system services. Any discovered method to bypass this firewall is considered a **High Severity** security vulnerability.

---
*Thank you for helping keep PowerTune safe.*
