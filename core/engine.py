import os
import sys
import subprocess
import re
import json
import datetime
try:
    import yaml
except ImportError:
    yaml = None

class JsonLogger:
    def __init__(self, log_dir):
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, "changes.log")
        
    def log(self, action, result, risk, why):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "action": action,
            "result": result,
            "risk": risk,
            "why": why
        }
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')

CRITICAL_SERVICES_BLOCKLIST = {
    "windefend", "mpssvc", "wuauserv", "dhcp", "rpcss", 
    "dcomlaunch", "plugplay", "audiosrv", "winmgmt", "wscsvc"
}

def run_powershell(script, args=None, timeout=10.0):
    cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", script]
    if args:
        cmd.extend(args)
    subprocess.run(cmd, timeout=timeout, check=True)

class BaseTweak:
    def __init__(self, tweak_data, logger=None):
        self.risk = tweak_data.get('risk', 'Unknown')
        self.why = tweak_data.get('why', '')
        self.logger = logger

    def execute(self, apply_changes):
        raise NotImplementedError

class CpuMinStateTweak(BaseTweak):
    def __init__(self, tweak_data, logger=None):
        super().__init__(tweak_data, logger)
        self.val = tweak_data.get('value')

    def execute(self, apply_changes):
        if apply_changes:
            subprocess.run(["powercfg", "/setdcvalueindex", "SCHEME_CURRENT", "SUB_PROCESSOR", "PROCTHROTTLEMIN", str(self.val)], timeout=5.0, check=True)
            subprocess.run(["powercfg", "/setacvalueindex", "SCHEME_CURRENT", "SUB_PROCESSOR", "PROCTHROTTLEMIN", str(self.val)], timeout=5.0, check=True)
            subprocess.run(["powercfg", "/setactive", "SCHEME_CURRENT"], timeout=5.0, check=True)
            print(f"     [+] Lowered CPU Minimum State to {self.val}% (Risk: {self.risk})")
            if self.logger:
                self.logger.log(f"Set CPU Min State to {self.val}%", "Success", self.risk, self.why)
        else:
            print(f"     [+] (Dry-Run) Would lower CPU Minimum State to {self.val}% (Risk: {self.risk})")
        print(f"         WHY: {self.why}")

class CpuMaxStateTweak(BaseTweak):
    def __init__(self, tweak_data, logger=None):
        super().__init__(tweak_data, logger)
        self.val = tweak_data.get('value')

    def execute(self, apply_changes):
        if apply_changes:
            subprocess.run(["powercfg", "/setdcvalueindex", "SCHEME_CURRENT", "SUB_PROCESSOR", "PROCTHROTTLEMAX", str(self.val)], timeout=5.0, check=True)
            subprocess.run(["powercfg", "/setacvalueindex", "SCHEME_CURRENT", "SUB_PROCESSOR", "PROCTHROTTLEMAX", str(self.val)], timeout=5.0, check=True)
            subprocess.run(["powercfg", "/setactive", "SCHEME_CURRENT"], timeout=5.0, check=True)
            print(f"     [+] Capped CPU Max State to {self.val}% (Risk: {self.risk})")
            if self.logger:
                self.logger.log(f"Set CPU Max State to {self.val}%", "Success", self.risk, self.why)
        else:
            print(f"     [+] (Dry-Run) Would cap CPU Max State to {self.val}% (Risk: {self.risk})")
        print(f"         WHY: {self.why}")

class ActiveSchemeTweak(BaseTweak):
    def __init__(self, tweak_data, logger=None):
        super().__init__(tweak_data, logger)
        self.guid = tweak_data.get('guid')
        self.name = tweak_data.get('name', 'Custom')

    def execute(self, apply_changes):
        if apply_changes:
            subprocess.run(["powercfg", "/setactive", self.guid], timeout=5.0, check=True)
            print(f"     [+] Switched to {self.name} Scheme (Risk: {self.risk})")
            if self.logger:
                self.logger.log(f"Switched Power Scheme to {self.name}", "Success", self.risk, self.why)
        else:
            print(f"     [+] (Dry-Run) Would switch to {self.name} Scheme (Risk: {self.risk})")
        print(f"         WHY: {self.why}")

class ServiceDisableTweak(BaseTweak):
    def __init__(self, tweak_data, logger=None):
        super().__init__(tweak_data, logger)
        self.target = tweak_data.get('target', '')

    def execute(self, apply_changes):
        if not re.match(r'^[a-zA-Z0-9.\-_]+$', self.target):
            if self.logger: self.logger.log(f"Disable service {self.target}", "Blocked: Injection attempt", "Critical", "")
            print(f"     [!] SECURITY VIOLATION: Invalid service name format '{self.target}'. Command injection blocked.")
            sys.exit(1)
            
        if self.target.lower() in CRITICAL_SERVICES_BLOCKLIST:
            if self.logger: self.logger.log(f"Disable service {self.target}", "Blocked: Critical service", "Critical", "")
            print(f"     [!] SECURITY VIOLATION: Blocked attempt to disable critical service '{self.target}'.")
            print("         See docs/SAFETY_POLICY.md for rules. Execution halted.")
            sys.exit(1)
            
        if apply_changes:
            subprocess.run(["powershell", "-Command", f"Stop-Service -Name {self.target} -Force -ErrorAction SilentlyContinue"], timeout=10.0, check=True)
            print(f"     [+] Stopped Service: {self.target} (Risk: {self.risk})")
            if self.logger:
                self.logger.log(f"Stopped service {self.target}", "Success", self.risk, self.why)
        else:
            print(f"     [+] (Dry-Run) Would stop service: {self.target} (Risk: {self.risk})")
        print(f"         WHY: {self.why}")

TWEAK_REGISTRY = {
    'cpu_min_state': CpuMinStateTweak,
    'cpu_max_state': CpuMaxStateTweak,
    'active_scheme': ActiveSchemeTweak,
    'service_disable': ServiceDisableTweak
}

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

    logger = JsonLogger(os.path.join(root_dir, "reports")) if apply_changes else None

    if apply_changes:
        run_powershell(os.path.join(root_dir, "rollback", "snapshot.ps1"), ["-Profile", profile.get("profile", "unknown")])
        if logger: logger.log("Generated Snapshot", "Success", "None", "Atomic state capture before execution")

    try:
        for tweak_data in profile.get('tweaks', []):
            tweak_id = tweak_data.get('id')
            tweak_class = TWEAK_REGISTRY.get(tweak_id)
            if tweak_class:
                tweak = tweak_class(tweak_data, logger)
                tweak.execute(apply_changes)
            else:
                print(f"     [!] Unknown tweak ID: {tweak_id}")
    except Exception as e:
        print(f"     [!] FATAL ERROR during profile execution: {e}")
        if apply_changes:
            print("     [*] ATOMIC ROLLBACK INITIATED: Reverting system to snapshot...")
            if logger: logger.log("Atomic Rollback Triggered", "Failed Execution", "High", str(e))
            run_powershell(os.path.join(root_dir, "rollback", "restore.ps1"), ["-Apply"])
            sys.exit(1)

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
