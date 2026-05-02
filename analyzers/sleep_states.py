import subprocess
import json
import argparse

def analyze_sleep_states(json_mode=False):
    telemetry = []
    try:
        # Event ID 1: System Sleep, Event ID 42: Kernel-Power entering sleep, Event ID 507: Modern Standby exit
        # We look for recent wake sources.
        ps_script = """
        Get-WinEvent -ProviderName "Microsoft-Windows-Power-Troubleshooter" -MaxEvents 3 -ErrorAction SilentlyContinue | 
        Select-Object TimeCreated, Message | ConvertTo-Json
        """
        output = subprocess.check_output(["powershell", "-Command", ps_script], text=True, timeout=10.0).strip()
        
        if output:
            events = json.loads(output)
            if isinstance(events, dict): events = [events]
            for event in events:
                msg = event.get("Message", "")
                source = "Unknown"
                if "Wake Source:" in msg:
                    source = msg.split("Wake Source:")[1].strip().split('\n')[0]
                
                severity = "high" if "Device" in source or "Timer" in source else "info"
                telemetry.append({
                    "category": "sleep_state",
                    "severity": severity,
                    "source": source,
                    "message": f"Recent Wake Event at {event.get('TimeCreated')}"
                })
        else:
            telemetry.append({
                "category": "sleep_state",
                "severity": "info",
                "source": "system",
                "message": "No recent wake events found."
            })
    except Exception as e:
        telemetry.append({
            "category": "sleep_state",
            "severity": "medium",
            "source": "system",
            "message": f"Could not read wake events: {e}"
        })
        
    if json_mode:
        print(json.dumps(telemetry))
        return telemetry
        
    print("     [*] Analyzing Sleep States & Wake Sources...")
    for t in telemetry:
        if t['severity'] == 'high':
            print(f"     [!] WARNING: {t['source']} caused a recent system wake.")
        else:
            print(f"     [+] {t['message']} (Source: {t['source']})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    analyze_sleep_states(args.json)
