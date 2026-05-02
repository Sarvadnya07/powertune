import subprocess
import json
import argparse
import time

def analyze_anomalies(json_mode=False):
    telemetry = []
    try:
        # Check for sustained high CPU usage by background processes (potential miner or runaway telemetry)
        ps_script = """
        Get-Process | Where-Object { $_.CPU -gt 100 -and $_.ProcessName -notmatch "chrome|code|devenv|firefox|msedge|Idle|System" } | 
        Sort-Object CPU -Descending | Select-Object -First 3 ProcessName, CPU | ConvertTo-Json -Compress
        """
        output = subprocess.check_output(["powershell", "-Command", ps_script], text=True, timeout=10.0).strip()
        
        if output:
            try:
                events = json.loads(output)
                if isinstance(events, dict): events = [events]
                for event in events:
                    name = event.get("ProcessName", "Unknown")
                    cpu_time = event.get("CPU", 0)
                    if cpu_time > 500: # Arbitrary high CPU time threshold
                        telemetry.append({
                            "category": "anomaly",
                            "severity": "high",
                            "source": name,
                            "message": f"Suspicious sustained background CPU usage detected ({cpu_time}s CPU time). Potential miner or memory leak."
                        })
            except json.JSONDecodeError:
                pass

        # If no anomalies found
        if not telemetry:
            telemetry.append({
                "category": "anomaly",
                "severity": "info",
                "source": "system",
                "message": "No sustained anomalous CPU workloads detected."
            })

    except Exception as e:
        telemetry.append({
            "category": "anomaly",
            "severity": "medium",
            "source": "system",
            "message": f"Could not complete anomaly scan: {e}"
        })
        
    if json_mode:
        print(json.dumps(telemetry))
        return telemetry
        
    print("     [*] Analyzing System Anomalies & Crypto Miners...")
    for t in telemetry:
        if t['severity'] == 'high':
            print(f"     [!] WARNING: {t['message']}")
        else:
            print(f"     [+] {t['message']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    analyze_anomalies(args.json)
