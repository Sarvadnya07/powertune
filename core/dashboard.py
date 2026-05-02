import os
import sys
import json
import webbrowser
from telemetry import collect_telemetry

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PowerTune Interactive Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #58a6ff;
            text-align: center;
            border-bottom: 1px solid #30363d;
            padding-bottom: 10px;
        }
        .container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .card h2 {
            margin-top: 0;
            font-size: 1.2rem;
            color: #8b949e;
        }
        .log-entry {
            padding: 8px;
            border-bottom: 1px solid #30363d;
            font-size: 0.9rem;
        }
        .log-entry:last-child {
            border-bottom: none;
        }
        .badge {
            display: inline-block;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: bold;
            margin-right: 10px;
        }
        .badge-info { background-color: #1f6feb; color: #fff; }
        .badge-medium { background-color: #d29922; color: #fff; }
        .badge-high { background-color: #da3633; color: #fff; }
    </style>
</head>
<body>

    <h1>🔋 PowerTune Systems Observability</h1>
    
    <div class="container">
        <!-- Severity Chart -->
        <div class="card">
            <h2>Telemetry Severity Breakdown</h2>
            <canvas id="severityChart"></canvas>
        </div>

        <!-- Telemetry Feed -->
        <div class="card">
            <h2>Live Diagnostics Stream</h2>
            <div id="telemetryFeed" style="max-height: 400px; overflow-y: auto;">
                <!-- Injected via JS -->
            </div>
        </div>
    </div>

    <script>
        // Data injected by Python
        const telemetryData = __TELEMETRY_JSON__;

        // Render Feed
        const feed = document.getElementById('telemetryFeed');
        let severityCounts = { 'info': 0, 'medium': 0, 'high': 0 };

        telemetryData.forEach(item => {
            const div = document.createElement('div');
            div.className = 'log-entry';
            
            const sev = item.severity || 'info';
            if (severityCounts[sev] !== undefined) severityCounts[sev]++;

            div.innerHTML = `
                <span class="badge badge-${sev}">${sev.toUpperCase()}</span>
                <strong>[${item.category.toUpperCase()}]</strong> 
                ${item.message} <em>(${item.source})</em>
            `;
            feed.appendChild(div);
        });

        // Render Chart
        const ctx = document.getElementById('severityChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Info', 'Medium', 'High / Critical'],
                datasets: [{
                    data: [severityCounts.info, severityCounts.medium, severityCounts.high],
                    backgroundColor: ['#1f6feb', '#d29922', '#da3633'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom', labels: { color: '#c9d1d9' } }
                }
            }
        });
    </script>
</body>
</html>
"""

def generate_dashboard(root_dir="."):
    print("     [*] Generating HTML/JS Observability Dashboard...")
    
    reports_dir = os.path.join(root_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    # 1. Collect live data
    data = collect_telemetry(root_dir)
    json_payload = json.dumps(data)
    
    # 2. Inject into HTML
    html_content = HTML_TEMPLATE.replace("__TELEMETRY_JSON__", json_payload)
    
    # 3. Save file
    output_path = os.path.join(reports_dir, "dashboard.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"     [+] Dashboard compiled successfully: {output_path}")
    
    # 4. Open in browser
    abs_path = os.path.abspath(output_path)
    file_uri = f"file:///{abs_path.replace(os.sep, '/')}"
    print(f"     [*] Launching browser: {file_uri}")
    webbrowser.open(file_uri)

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    generate_dashboard(root)
