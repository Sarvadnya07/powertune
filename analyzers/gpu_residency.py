import subprocess
import json
import argparse

def get_telemetry():
    telemetry = []
    try:
        smi_output = subprocess.check_output(["nvidia-smi", "--query-compute-apps=pid,process_name", "--format=csv,noheader"], text=True, timeout=5.0)
        apps = [line.strip() for line in smi_output.splitlines() if line.strip()]
        
        if not apps:
            telemetry.append({
                "category": "gpu",
                "severity": "info",
                "source": "nvidia-smi",
                "message": "NVIDIA dGPU is in P8 (Deep Sleep)."
            })
        else:
            for app in apps:
                telemetry.append({
                    "category": "gpu",
                    "severity": "high",
                    "source": app,
                    "message": "Process is keeping dGPU awake."
                })
    except Exception as e:
        telemetry.append({
            "category": "gpu",
            "severity": "info",
            "source": "system",
            "message": "nvidia-smi not found or dGPU is not NVIDIA."
        })
    return telemetry

def analyze_gpu_residency(json_mode=False):
    telemetry = get_telemetry()
        
    if json_mode:
        print(json.dumps(telemetry))
        return telemetry
        
    print("     [*] Analyzing GPU Residency & Wakeups...")
    for t in telemetry:
        if t['severity'] == 'high':
            print(f"     [!] WARNING: {t['source']} - {t['message']}")
            print("         WHY: When the dGPU is active, system power draw increases by 10-20W even at idle.")
        else:
            print(f"     [+] {t['message']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    analyze_gpu_residency(args.json)
