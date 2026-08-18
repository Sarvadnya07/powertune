## Security Architecture
- **No Remote Execution:** PowerTune intentionally lacks a network listener by default to eliminate RCE vectors.
- **Privilege Separation:** UI processes run as standard users; only the core data collection engine requests elevation.
- **Anti-Timing Attacks:** Cryptographic validations in 	ests/test_security.py ensure profile validations are done in constant time.

## Handling Sensitivities
We actively strip out personally identifiable information (PII) such as file paths and user SIDs from ETW traces before local storage or analysis.
