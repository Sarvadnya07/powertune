import subprocess
import json
import argparse

def analyze_power_attribution(json_mode=False):
    telemetry = []
    try:
        # Use PowerShell to grab process metrics. 
        # Win32_PerfFormattedData_PerfProc_Process contains PercentProcessorTime which is a great proxy for power usage.
        ps_script = """
        Get-WmiObject Win32_PerfFormattedData_PerfProc_Process | 
        Where-Object { $_.PercentProcessorTime -gt 5 -and $_.Name -notmatch "Idle|_Total|System" } | 
        Sort-Object PercentProcessorTime -Descending | Select-Object -First 3 Name, PercentProcessorTime | ConvertTo-Json -Compress
        """
        output = subprocess.check_output(["powershell", "-Command", ps_script], text=True, timeout=10.0).strip()
        
        if output:
            try:
                events = json.loads(output)
                if isinstance(events, dict): events = [events]
                for event in events:
                    name = event.get("Name", "Unknown")
                    cpu_percent = event.get("PercentProcessorTime", 0)
                    
                    # Estimate wattage impact (rough proxy: 1% CPU time on modern processors is ~0.1W - 0.5W depending on TDP)
                    # We classify anything actively drawing sustained time as high drain.
                    telemetry.append({
                        "category": "power_attribution",
                        "severity": "medium" if cpu_percent < 20 else "high",
                        "source": name,
                        "message": f"Process is actively draining battery ({cpu_percent}% CPU Time)."
                    })
            except json.JSONDecodeError:
                pass

        if not telemetry:
            telemetry.append({
                "category": "power_attribution",
                "severity": "info",
                "source": "system",
                "message": "Power distribution is optimal. No single process is dominating battery drain."
            })

    except Exception as e:
        telemetry.append({
            "category": "power_attribution",
            "severity": "medium",
            "source": "system",
            "message": f"Could not calculate power attribution: {e}"
        })
        
    if json_mode:
        print(json.dumps(telemetry))
        return telemetry
        
    print("     [*] Analyzing Process Power Attribution...")
    for t in telemetry:
        if t['severity'] == 'high':
            print(f"     [!] WARNING: {t['message']} (Source: {t['source']})")
        elif t['severity'] == 'medium':
            print(f"     [-] NOTICE: {t['message']} (Source: {t['source']})")
        else:
            print(f"     [+] {t['message']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    analyze_power_attribution(args.json)
