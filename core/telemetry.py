try:
    from core.ui import display_analyzer_results, show_recommendation_panel, console
    UI_AVAILABLE = True
except ImportError:
    UI_AVAILABLE = False

def collect_telemetry(root_dir="."):
    analyzers_dir = os.path.join(root_dir, "analyzers")
    # Dynamically find all .py files in analyzers/
    scripts = [f for f in os.listdir(analyzers_dir) if f.endswith(".py") and f != "__init__.py"]
    
    master_telemetry = []
    
    if not UI_AVAILABLE:
        print("     [*] Running Unified Telemetry Diagnostics...")
    
    for script in scripts:
        script_path = os.path.join(analyzers_dir, script)
        try:
            # Determine python command
            py_cmd = sys.executable if sys.executable else "python"
            out = subprocess.check_output([py_cmd, script_path, "--json"], text=True, timeout=15.0)
            for line in out.splitlines():
                if line.startswith("[") and line.endswith("]"):
                    data = json.loads(line)
                    master_telemetry.extend(data)
        except Exception:
            pass
                
    return master_telemetry

def generate_recommendations(telemetry):
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
    else:
        print("     [*] Severity Classification & Recommendations:")
        for t in telemetry:
            if t.get('severity') in ['high', 'critical']:
                print(f"         [!] {t['category'].upper()}: {t['message']} (Source: {t['source']})")

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    data = collect_telemetry(root)
    generate_recommendations(data)
