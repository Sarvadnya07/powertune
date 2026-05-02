import os
import sys
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.engine import execute_profile

def test_security_sandbox():
    mock_yaml = """
profile: malicious
description: Attempts to disable Windows Defender
tweaks:
  - id: service_disable
    target: "WinDefend"
    risk: High
    why: "Because I am a bad script."
"""
    test_file = "test_malicious.yaml"
    with open(test_file, "w") as f:
        f.write(mock_yaml)
        
    try:
        print("[*] Testing Security Sandbox against malicious YAML...")
        # We expect a SystemExit to be raised when the blocklist is hit
        try:
            execute_profile(test_file, apply_changes=False)
            assert False, "SecurityViolation was not raised!"
        except SystemExit:
            print("[+] Security Sandbox successfully blocked the malicious action.")
    finally:
        os.remove(test_file)

if __name__ == "__main__":
    test_security_sandbox()
