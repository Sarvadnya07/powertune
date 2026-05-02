import subprocess
import json
import argparse

def get_telemetry():
    telemetry = []
    try:
        # Many modern Windows systems expose thermal zones via MSAcpi_ThermalZoneTemperature
        # The temperature is returned in tenths of degrees Kelvin.
        ps_script = """
        Get-WmiObject -Namespace root/wmi -Class MSAcpi_ThermalZoneTemperature -ErrorAction SilentlyContinue | 
        Select-Object InstanceName, CurrentTemperature | ConvertTo-Json -Compress
        """
        output = subprocess.check_output(["powershell", "-Command", ps_script], text=True, timeout=5.0).strip()
        
        if output:
            try:
                zones = json.loads(output)
                if isinstance(zones, dict): zones = [zones]
                
                max_temp_c = 0
                for zone in zones:
                    # Convert from tenths of Kelvin to Celsius
                    temp_k = zone.get("CurrentTemperature", 0) / 10.0
                    temp_c = temp_k - 273.15
                    
                    if temp_c > max_temp_c:
                        max_temp_c = temp_c

                if max_temp_c > 90:
                    telemetry.append({
                        "category": "thermal",
                        "severity": "critical",
                        "source": "ACPI Thermal Zone",
                        "message": f"CRITICAL: Severe thermal saturation detected ({max_temp_c:.1f}°C). System is likely throttling."
                    })
                elif max_temp_c > 75:
                    telemetry.append({
                        "category": "thermal",
                        "severity": "medium",
                        "source": "ACPI Thermal Zone",
                        "message": f"WARNING: High thermal load ({max_temp_c:.1f}°C). Cooling efficiency may be compromised."
                    })
                else:
                    telemetry.append({
                        "category": "thermal",
                        "severity": "info",
                        "source": "ACPI Thermal Zone",
                        "message": f"Thermals are optimal (Max: {max_temp_c:.1f}°C)."
                    })
            except json.JSONDecodeError:
                pass
        
        if not telemetry:
            # Fallback if ACPI is blocked by vendor firmware (very common on ASUS/Lenovo)
            telemetry.append({
                "category": "thermal",
                "severity": "info",
                "source": "system",
                "message": "Thermal sensors are abstracted by vendor firmware (Requires OEM module to read)."
            })

    except Exception as e:
        telemetry.append({
            "category": "thermal",
            "severity": "medium",
            "source": "system",
            "message": f"Could not read thermal probes: {e}"
        })
    return telemetry

def analyze_thermals(json_mode=False):
    telemetry = get_telemetry()
        
    if json_mode:
        print(json.dumps(telemetry))
        return telemetry
        
    print("     [*] Analyzing Thermal Cooling Efficiency...")
    for t in telemetry:
        if t['severity'] in ['critical', 'high']:
            print(f"     [!] WARNING: {t['message']}")
        elif t['severity'] == 'medium':
            print(f"     [-] NOTICE: {t['message']}")
        else:
            print(f"     [+] {t['message']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    analyze_thermals(args.json)
