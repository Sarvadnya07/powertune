import subprocess

BLOAT_SERVICES = ["ArmouryCrate.Service", "LightingService", "SupportAssist", "HPAppHelper"]

def check_services():
    print("     [*] Analyzing background services...")
    found = False
    try:
        output = subprocess.check_output(["powershell", "-Command", "Get-Service | Select-Object Name, Status"], text=True, timeout=15.0)
        for line in output.splitlines():
            for bloat in BLOAT_SERVICES:
                if bloat in line and "Running" in line:
                    print(f"     [!] Found bloat service running: {bloat}")
                    print(f"         WHY: This service is known to cause excess CPU wakeups.")
                    found = True
        if not found:
            print("     [+] No known bloat services found running.")
    except Exception as e:
         print("     [!] Could not check services.")

if __name__ == "__main__":
    check_services()
