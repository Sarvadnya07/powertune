import os
import sys
import subprocess
try:
    import yaml
except ImportError:
    yaml = None

CRITICAL_SERVICES_BLOCKLIST = {
    "windefend", "mpssvc", "wuauserv", "dhcp", "rpcss", 
    "dcomlaunch", "plugplay", "audiosrv", "winmgmt", "wscsvc"
}

def run_powershell(script, args=None):
    cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", script]
    if args:
        cmd.extend(args)
    subprocess.run(cmd)

def execute_profile(yaml_path, apply_changes=False, root_dir="."):
    if not yaml:
        print("     [!] PyYAML is not installed. Run 'pip install pyyaml'.")
        return
    
    if not os.path.exists(yaml_path):
        print(f"     [!] Profile not found: {yaml_path}")
        return

    with open(yaml_path, 'r', encoding='utf-8') as f:
        profile = yaml.safe_load(f)

    print(f"     [*] Configuring Profile: {profile.get('profile', 'Unknown').upper()}...")
    print(f"         {profile.get('description', '')}")

    if apply_changes:
        run_powershell(os.path.join(root_dir, "rollback", "snapshot.ps1"), ["-Profile", profile.get("profile", "unknown")])

    for tweak in profile.get('tweaks', []):
        tweak_id = tweak.get('id')
        risk = tweak.get('risk', 'Unknown')
        why = tweak.get('why', '')
        
        if tweak_id == 'cpu_min_state':
            val = tweak.get('value')
            if apply_changes:
                subprocess.run(["powercfg", "/setdcvalueindex", "SCHEME_CURRENT", "SUB_PROCESSOR", "PROCTHROTTLEMIN", str(val)])
                subprocess.run(["powercfg", "/setacvalueindex", "SCHEME_CURRENT", "SUB_PROCESSOR", "PROCTHROTTLEMIN", str(val)])
                subprocess.run(["powercfg", "/setactive", "SCHEME_CURRENT"])
                print(f"     [+] Lowered CPU Minimum State to {val}% (Risk: {risk})")
                print(f"         WHY: {why}")
            else:
                print(f"     [+] (Dry-Run) Would lower CPU Minimum State to {val}% (Risk: {risk})")
                print(f"         WHY: {why}")
                
        elif tweak_id == 'cpu_max_state':
            val = tweak.get('value')
            if apply_changes:
                subprocess.run(["powercfg", "/setdcvalueindex", "SCHEME_CURRENT", "SUB_PROCESSOR", "PROCTHROTTLEMAX", str(val)])
                subprocess.run(["powercfg", "/setacvalueindex", "SCHEME_CURRENT", "SUB_PROCESSOR", "PROCTHROTTLEMAX", str(val)])
                subprocess.run(["powercfg", "/setactive", "SCHEME_CURRENT"])
                print(f"     [+] Capped CPU Max State to {val}% (Risk: {risk})")
                print(f"         WHY: {why}")
            else:
                print(f"     [+] (Dry-Run) Would cap CPU Max State to {val}% (Risk: {risk})")
                print(f"         WHY: {why}")
                
        elif tweak_id == 'active_scheme':
            guid = tweak.get('guid')
            name = tweak.get('name', 'Custom')
            if apply_changes:
                subprocess.run(["powercfg", "/setactive", guid])
                print(f"     [+] Switched to {name} Scheme (Risk: {risk})")
                print(f"         WHY: {why}")
            else:
                print(f"     [+] (Dry-Run) Would switch to {name} Scheme (Risk: {risk})")
                print(f"         WHY: {why}")
                
        elif tweak_id == 'service_disable':
            target = tweak.get('target', '')
            if target.lower() in CRITICAL_SERVICES_BLOCKLIST:
                print(f"     [!] SECURITY VIOLATION: Blocked attempt to disable critical service '{target}'.")
                print("         See docs/SAFETY_POLICY.md for rules. Execution halted.")
                sys.exit(1)
                
            if apply_changes:
                subprocess.run(["powershell", "-Command", f"Stop-Service -Name {target} -Force -ErrorAction SilentlyContinue"])
                print(f"     [+] Stopped Service: {target} (Risk: {risk})")
                print(f"         WHY: {why}")
            else:
                print(f"     [+] (Dry-Run) Would stop service: {target} (Risk: {risk})")
                print(f"         WHY: {why}")

    if apply_changes:
        print("     [+] Applied Profile successfully.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="PowerTune DSL Engine")
    parser.add_argument("profile_yaml", help="Path to profile YAML file")
    parser.add_argument("--apply", action="store_true", help="Apply changes (requires admin)")
    parser.add_argument("--root", default=".", help="Project root directory")
    args = parser.parse_args()
    
    execute_profile(args.profile_yaml, args.apply, args.root)
