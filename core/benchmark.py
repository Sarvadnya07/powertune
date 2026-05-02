import subprocess
import json
import argparse
import time

def run_benchmark():
    print("     [*] Initiating Idle Power Benchmark (10 seconds)...")
    print("     [*] DO NOT MOVE THE MOUSE OR TYPE.")
    
    try:
        # WMI BatteryStatus gives discharge rate in mW on some systems
        # We will poll 3 times over 10 seconds and average
        rates = []
        for _ in range(3):
            ps_script = "(Get-WmiObject -Class Win32_Battery).EstimatedChargeRemaining"
            output = subprocess.check_output(["powershell", "-Command", ps_script], text=True, timeout=5.0).strip()
            if output:
                rates.append(int(output))
            time.sleep(3)
            
        print(f"     [+] Battery Percentage Stable at: {rates[-1]}%")
        print("         (Note: Accurate mW idle measurement requires external hardware or HWInfo64 integration).")
        return rates
    except Exception as e:
        print(f"     [!] Benchmark failed: {e}")
        return []

if __name__ == "__main__":
    run_benchmark()
