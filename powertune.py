import argparse
import sys
import os

from core.telemetry import collect_telemetry, generate_recommendations
from core.engine import execute_profile
from core.ui import console, display_analyzer_results, show_recommendation_panel

def main():
    parser = argparse.ArgumentParser(description="PowerTune - Systems Observability & Power Intelligence")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Run full diagnostic suite")
    
    # profile commands
    battery_parser = subparsers.add_parser("battery", help="Apply battery-saver profile")
    battery_parser.add_argument("--apply", action="store_true", help="Apply changes (requires admin)")
    
    gaming_parser = subparsers.add_parser("gaming", help="Apply gaming performance profile")
    gaming_parser.add_argument("--apply", action="store_true", help="Apply changes (requires admin)")

    dev_parser = subparsers.add_parser("dev", help="Apply developer profile")
    dev_parser.add_argument("--apply", action="store_true", help="Apply changes (requires admin)")

    history_parser = subparsers.add_parser("history", help="View historical diagnostic events")
    history_parser.add_argument("--limit", type=int, default=10, help="Number of events to show")

    args = parser.parse_args()
    
    console.print("\n[bold cyan]  POWERTUNE - Systems Observability & Power Intelligence[/bold cyan]")
    console.print("  [dim]Safe, explainable, reversible laptop optimization & diagnostics.[/dim]\n")
    
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    if args.command == "analyze":
        console.print("  [bold cyan][>] Diagnostic Analyzer[/bold cyan]\n")
        data = collect_telemetry(root_dir)
        generate_recommendations(data, root_dir)
        
    elif args.command == "history":
        from core.database import TelemetryDB
        from rich.table import Table
        db = TelemetryDB(root_dir)
        events = db.get_recent_events(args.limit)
        
        table = Table(title="[bold cyan]Historical Diagnostic Events[/bold cyan]")
        table.add_column("Timestamp", style="dim")
        table.add_column("Category")
        table.add_column("Severity")
        table.add_column("Source")
        table.add_column("Message", ratio=1)
        
        for e in events:
            # Color severity
            sev = e[2].lower()
            color = "white"
            if sev == "high": color = "red"
            elif sev == "medium": color = "yellow"
            elif sev == "info": color = "green"
            
            table.add_row(e[0], e[1], f"[{color}]{e[2].upper()}[/{color}]", e[3], e[4])
        
        console.print(table)
        
    elif args.command in ["battery", "gaming", "dev"]:
        profile_map = {"battery": "battery", "gaming": "gaming", "dev": "developer"}
        yaml_path = os.path.join(root_dir, "profiles", f"{profile_map[args.command]}.yaml")
        
        console.print(f"  [bold cyan][>] {args.command.capitalize()} Profile[/bold cyan]\n")
        try:
            execute_profile(yaml_path, args.apply, root_dir)
        except Exception as e:
            console.print(f"  [bold red][!] FATAL ERROR: {e}[/bold red]")

if __name__ == "__main__":
    main()
