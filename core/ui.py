from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich import box
import json

console = Console()

def print_banner():
    banner = """
  [cyan]██████╗  ██████╗ ██╗    ██╗███████╗██████╗ ████████╗██╗   ██╗███╗   ██╗███████╗[/cyan]
  [cyan]██╔══██╗██╔═══██╗██║    ██║██╔════╝██╔══██╗╚══██╔══╝██║   ██║████╗  ██║██╔════╝[/cyan]
  [cyan]██████╔╝██║   ██║██║ █╗ ██║█████╗  ██████╔╝   ██║   ██║   ██║██╔██╗ ██║█████╗  [/cyan]
  [cyan]██╔═══╝ ██║   ██║██║███╗██║██╔══╝  ██╔══██╗   ██║   ██║   ██║██║╚██╗██║██╔══╝  [/cyan]
  [cyan]██║     ╚██████╔╝╚███╔███╔╝███████╗██║  ██║   ██║   ╚██████╔╝██║ ╚████║███████╗[/cyan]
  [cyan]╚═╝      ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚══════╝[/cyan]
    """
    console.print(banner)
    console.print("  [grey50]Safe, explainable, reversible laptop optimization & diagnostics.[/grey50]")
    console.print("  [grey37]v1.1.0  |  MIT License  |  https://github.com/Sarvadnya07/powertune[/grey37]")
    console.print("\n" + "─" * 80, style="grey37")

def display_analyzer_results(title, results):
    table = Table(title=f"[bold cyan]{title}[/bold cyan]", box=box.ROUNDED, show_header=True, header_style="bold magenta")
    table.add_column("Category", style="dim")
    table.add_column("Source")
    table.add_column("Severity")
    table.add_column("Message", ratio=1)
    table.add_column("Intelligence (Root Cause)", ratio=1, style="italic dim")

    from core.intelligence import RootCauseEngine
    engine = RootCauseEngine()

    for item in results:
        severity = item.get('severity', 'info').lower()
        color = "white"
        if severity == "critical": color = "bold red"
        elif severity == "high": color = "red"
        elif severity == "medium": color = "yellow"
        elif severity == "info": color = "green"
        
        root_cause = engine.analyze(item)
        
        table.add_row(
            item.get('category', 'N/A'),
            item.get('source', 'N/A'),
            f"[{color}]{severity.upper()}[/{color}]",
            item.get('message', ''),
            root_cause
        )
    
    console.print(table)

def show_recommendation_panel(recommendations):
    content = ""
    for rec in recommendations:
        content += f"• [bold yellow]{rec['title']}[/bold yellow]: {rec['description']}\n"
        content += f"  [dim]Rationale: {rec['why']}[/dim]\n\n"
    
    panel = Panel(content, title="[bold green]AI Recommendation Engine[/bold green]", border_style="green", box=box.HEAVY)
    console.print(panel)

class LiveDiagnosticUI:
    def __init__(self):
        self.layout = Layout()
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        )
    
    def start_diagnostic_session(self):
        with Live(self.layout, refresh_per_second=4):
            self.layout["header"].update(Panel("[bold cyan]PowerTune Diagnostic Suite[/bold cyan]", box=box.SIMPLE))
            self.layout["footer"].update(Panel("[dim]Press Ctrl+C to abort diagnostic sequence[/dim]", box=box.SIMPLE))
            # Logic to update body with results as they come in...
