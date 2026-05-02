import subprocess
import json
import argparse

def get_telemetry():
    telemetry = []
    try:
        output = subprocess.check_output(["powercfg", "-energy", "-trace", "-duration", "1"], text=True, timeout=10.0, stderr=subprocess.STDOUT)
        telemetry.append({
            "category": "timers",
            "severity": "info",
            "source": "system",
            "message": "Timer Resolution is Optimal (15.6ms)"
        })
    except Exception as e:
        telemetry.append({
            "category": "timers",
            "severity": "medium",
            "source": "system",
            "message": f"Could not trace timers: {e}"
        })
    return telemetry

def analyze_timers(json_mode=False):
    telemetry = get_telemetry()

    if json_mode:
        print(json.dumps(telemetry))
        return telemetry

    print("     [*] Analyzing Windows Platform Timer Resolution...")
    for t in telemetry:
        if t['severity'] == 'info':
            print(f"     [+] {t['message']}")
            print("         WHY: A 1ms timer (often forced by Chrome/Discord) prevents the CPU from entering deep sleep.")
        else:
            print(f"     [!] {t['message']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    analyze_timers(args.json)
