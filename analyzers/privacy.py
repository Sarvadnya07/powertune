import subprocess
import json
import argparse

def get_telemetry():
    telemetry = []
    
    # 1. Check for active ETW Telemetry Providers (e.g., Microsoft.Windows.Privacy.Diagnostic)
    # 2. Check for known vendor telemetry services (e.g., DiagTrack, AsusCert, etc.)
    
    privacy_offenders = {
        "DiagTrack": "Connected User Experiences and Telemetry (Microsoft)",
        "dmwappushservice": "WAP Push Message Routing Service (Microsoft)",
        "AsusCertService": "ASUS Certificate Telemetry",
        "HPAnalytics": "HP Analytics Service",
        "DellClientManagementService": "Dell Telemetry Service"
    }
    
    try:
        found_services = []
        for svc_name, desc in privacy_offenders.items():
            ps_script = f"Get-Service -Name {svc_name} -ErrorAction SilentlyContinue | Select-Object Status"
            output = subprocess.check_output(["powershell", "-Command", ps_script], text=True, timeout=5.0).strip()
            
            if "Running" in output:
                telemetry.append({
                    "category": "privacy",
                    "severity": "medium",
                    "source": svc_name,
                    "message": f"Active Telemetry Service: {desc}. This service routinely collects and uploads system data."
                })
                found_services.append(svc_name)
        
        if not telemetry:
            telemetry.append({
                "category": "privacy",
                "severity": "info",
                "source": "system",
                "message": "No high-risk vendor telemetry services are currently active."
            })
            
    except Exception as e:
        telemetry.append({
            "category": "privacy",
            "severity": "medium",
            "source": "system",
            "message": f"Could not complete privacy scan: {e}"
        })
    return telemetry

def analyze_privacy(json_mode=False):
    telemetry = get_telemetry()
        
    if json_mode:
        print(json.dumps(telemetry))
        return telemetry
        
    print("     [*] Analyzing Telemetry & Privacy Exposure...")
    for t in telemetry:
        if t['severity'] == 'medium':
            print(f"     [!] NOTICE: {t['message']}")
        else:
            print(f"     [+] {t['message']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    analyze_privacy(args.json)
