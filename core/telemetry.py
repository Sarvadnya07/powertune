import os
import sys
import json
import subprocess

def collect_telemetry(root_dir="."):
    analyzers_dir = os.path.join(root_dir, "analyzers")
    scripts = ["gpu_residency.py", "sleep_states.py", "timers.py"]
    
    master_telemetry = []
    
    print("     [*] Running Unified Telemetry Diagnostics...")
    for script in scripts:
        script_path = os.path.join(analyzers_dir, script)
        if os.path.exists(script_path):
            try:
                out = subprocess.check_output(["python", script_path, "--json"], text=True, timeout=15.0)
                # Parse JSON blocks from output (some scripts might print other things, so we find the json)
                for line in out.splitlines():
                    if line.startswith("[") and line.endswith("]"):
                        data = json.loads(line)
                        master_telemetry.extend(data)
            except Exception as e:
                pass
                
    return master_telemetry

def generate_recommendations(telemetry):
    print("     [*] Severity Classification & Recommendations:")
    criticals = 0
    for t in telemetry:
        if t.get('severity') == 'high':
            criticals += 1
            print(f"         [!] {t['category'].upper()}: {t['message']} (Source: {t['source']})")
            
    if criticals == 0:
        print("         [+] System is running optimally. No critical power drains detected.")
    else:
        print(f"\n         REC: Generated {criticals} recommendations. Consider applying the 'battery.yaml' profile to restrict background timers and wakeups.")

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    data = collect_telemetry(root)
    generate_recommendations(data)
