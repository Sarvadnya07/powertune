import os
import sys
import json
import subprocess

if len(sys.argv) > 1:
    sys.path.insert(0, sys.argv[1])

try:
    from core.ui import display_analyzer_results, show_recommendation_panel, console
    from core.database import TelemetryDB
    UI_AVAILABLE = True
except ImportError:
    UI_AVAILABLE = False
    TelemetryDB = None

import concurrent.futures

import importlib.util

def run_analyzer(script_path):
    try:
        module_name = os.path.splitext(os.path.basename(script_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Check if the module exposes a specific get_telemetry or analyze method
        if hasattr(module, 'get_telemetry'):
            return module.get_telemetry()
            
        # Fallback to subprocess if not yet refactored
        py_cmd = sys.executable if sys.executable else "python"
        out = subprocess.check_output([py_cmd, script_path, "--json"], text=True, timeout=15.0, stderr=subprocess.STDOUT)
        results = []
        for line in out.splitlines():
            if line.startswith("[") and line.endswith("]"):
                data = json.loads(line)
                results.extend(data)
        return results
    except Exception as e:
        return []

def collect_telemetry(root_dir="."):
    analyzers_dir = os.path.join(root_dir, "analyzers")
    scripts = [
        "gpu_residency.py", "sleep_states.py", "timers.py", 
        "anomaly.py", "power_attribution.py", "thermal.py", 
        "privacy.py", "kernel_etw.py", "browser_intel.py"
    ]
    
    master_telemetry = []
    
    if not UI_AVAILABLE:
        print("     [*] Running Unified Telemetry Diagnostics...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(scripts) or 1) as executor:
        futures = [executor.submit(run_analyzer, os.path.join(analyzers_dir, script)) for script in scripts]
        for future in concurrent.futures.as_completed(futures):
            master_telemetry.extend(future.result())
    
    # Phase 10: Dynamic Plugin Execution
    from core.plugins import PluginManager
    pm = PluginManager(root_dir)
    plugin_results = pm.run_plugins()
    master_telemetry.extend(plugin_results)
    
    # Phase 2: Persist to Time-Series DB
    if TelemetryDB:
        db = TelemetryDB(root_dir)
        db.log_events(master_telemetry)
        
        # Attempt to capture real-time discharge metric if available in the batch
        for t in master_telemetry:
            if "Wear Level" in t.get('message', ''):
                # Custom logic for future battery metric normalization
                pass

    return master_telemetry

def generate_recommendations(telemetry, root_dir="."):
    if UI_AVAILABLE:
        display_analyzer_results("Unified System Telemetry", telemetry)
        
        # Heuristic recommendations
        recs = []
        high_severity = [t for t in telemetry if t.get('severity') in ['high', 'critical']]
        
        if high_severity:
            recs.append({
                "title": "Aggressive Power Profile Recommended",
                "description": "Multiple high-severity power drains detected.",
                "why": f"Found {len(high_severity)} issues including {high_severity[0]['category']} wakeups."
            })
        
        gpu_issues = [t for t in telemetry if t.get('category') == 'gpu' and t.get('severity') == 'high']
        if gpu_issues:
            recs.append({
                "title": "Discrete GPU Residency Alert",
                "description": "Apps are preventing your dGPU from entering deep sleep.",
                "why": f"Identified: {gpu_issues[0]['source']}. This can increase idle drain by 15W+."
            })

        if recs:
            show_recommendation_panel(recs)
        else:
            console.print("\n[bold green]✅ System Health Optimal:[/bold green] No critical bottlenecks identified.")
            
        # Phase 9: Predictive Analytics
        try:
            from core.predictions import PredictiveEngine
            engine = PredictiveEngine(root_dir)
            predictions = engine.get_recommendations()
            
            console.print("\n[bold cyan]FUTURE INTELLIGENCE & PREDICTIVE ANALYTICS[/bold cyan]")
            console.print(f"  * [bold white]Battery Outlook:[/bold white] {predictions['battery_prediction']}")
            console.print(f"  * [bold white]Thermal Outlook:[/bold white] {predictions['thermal_prediction']}\n")
        except Exception as e:
            console.print(f"\n[dim]Predictive Engine Unavailable: {e}[/dim]\n")
    else:
        print("     [*] Severity Classification & Recommendations:")
        for t in telemetry:
            if t.get('severity') in ['high', 'critical']:
                print(f"         [!] {t['category'].upper()}: {t['message']} (Source: {t['source']})")

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    data = collect_telemetry(root)
    generate_recommendations(data, root)
