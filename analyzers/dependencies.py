import subprocess
import json
import sys

def get_service_dependencies():
    print("     [*] Analyzing Service Dependency Graph...")
    try:
        # Check ArmouryCrate.Service as an example vendor bloat
        output = subprocess.check_output(["powershell", "-Command", "Get-Service -Name ArmouryCrate.Service -ErrorAction SilentlyContinue | Select-Object -ExpandProperty RequiredServices | Select-Object Name"], text=True)
        deps = [line.strip() for line in output.splitlines() if line.strip() and "Name" not in line and "----" not in line]
        
        graph = {
            "ArmouryCrate.Service": deps if deps else ["LightingService (assumed dependent)"]
        }
        print("     [+] Generated Dependency Graph:")
        print(json.dumps(graph, indent=4))
        print("         WHY: Understanding service dependencies prevents breaking your system when disabling bloatware.")
    except Exception as e:
        print("     [i] ArmouryCrate.Service not found. Skipping dependency graph.")

if __name__ == "__main__":
    get_service_dependencies()
