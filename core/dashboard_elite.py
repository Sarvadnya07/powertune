import os
import sys
import json
from telemetry import collect_telemetry
from database import TelemetryDB

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>PowerTune Elite | Observability Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0d1117;
            --card: #161b22;
            --border: #30363d;
            --text: #c9d1d9;
            --accent: #58a6ff;
            --success: #238636;
            --warning: #d29922;
            --danger: #da3633;
        }
        body {
            background: var(--bg);
            color: var(--text);
            font-family: 'Inter', sans-serif;
            margin: 0; padding: 40px;
        }
        .header {
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 40px; border-bottom: 1px solid var(--border);
            padding-bottom: 20px;
        }
        .grid {
            display: grid; grid-template-columns: 2fr 1fr; gap: 30px;
        }
        .card {
            background: var(--card); border: 1px solid var(--border);
            border-radius: 12px; padding: 25px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        }
        .metric-card {
            text-align: center; padding: 20px;
        }
        .metric-value {
            font-size: 2.5rem; font-weight: 600; color: var(--accent);
        }
        .metric-label { font-size: 0.9rem; color: #8b949e; margin-top: 5px; }
        .feed { max-height: 500px; overflow-y: auto; }
        .log-entry {
            padding: 12px; border-bottom: 1px solid var(--border);
            display: flex; gap: 15px; align-items: flex-start;
        }
        .badge {
            padding: 4px 8px; border-radius: 6px; font-size: 0.7rem;
            font-weight: 600; text-transform: uppercase; min-width: 60px; text-align: center;
        }
        .badge-high { background: rgba(218, 54, 51, 0.1); color: var(--danger); border: 1px solid var(--danger); }
        .badge-medium { background: rgba(210, 153, 34, 0.1); color: var(--warning); border: 1px solid var(--warning); }
        .badge-info { background: rgba(31, 111, 235, 0.1); color: var(--accent); border: 1px solid var(--accent); }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1 style="margin:0; color:var(--accent)">PowerTune <span style="font-weight:300">Elite</span></h1>
            <p style="margin:5px 0 0 0; color:#8b949e">Systems Intelligence & Observability Dashboard</p>
        </div>
        <div style="text-align:right">
            <div id="status-badge" class="badge badge-info">System Optimal</div>
            <p style="font-size:0.8rem; color:#8b949e; margin-top:8px" id="timestamp"></p>
        </div>
    </div>

    <div class="grid">
        <div class="card">
            <h2>Severity Intelligence</h2>
            <canvas id="severityChart" height="150"></canvas>
            <div style="display:flex; justify-content:space-around; margin-top:30px">
                <div class="metric-card">
                    <div class="metric-value" id="val-high">0</div>
                    <div class="metric-label">High Severity</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="val-med">0</div>
                    <div class="metric-label">Medium Risks</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="val-total">0</div>
                    <div class="metric-label">Total Events</div>
                </div>
            </div>
        </div>

        <div class="card feed">
            <h2>Diagnostic Stream</h2>
            <div id="telemetryFeed"></div>
        </div>
    </div>

    <script>
        const telemetryData = __TELEMETRY_JSON__;
        document.getElementById('timestamp').innerText = `Last Refreshed: ${new Date().toLocaleString()}`;

        const feed = document.getElementById('telemetryFeed');
        let counts = { info: 0, medium: 0, high: 0, critical: 0 };

        telemetryData.forEach(item => {
            const sev = (item.severity || 'info').toLowerCase();
            if(counts[sev] !== undefined) counts[sev]++;
            if(sev === 'critical') counts.high++;

            const div = document.createElement('div');
            div.className = 'log-entry';
            div.innerHTML = `
                <div class="badge badge-${sev === 'critical' ? 'high' : sev}">${sev}</div>
                <div>
                    <div style="font-weight:600; font-size:0.95rem">[${item.category.toUpperCase()}] ${item.source}</div>
                    <div style="color:#8b949e; font-size:0.85rem; margin-top:4px">${item.message}</div>
                </div>
            `;
            feed.appendChild(div);
        });

        document.getElementById('val-high').innerText = counts.high + counts.critical;
        document.getElementById('val-med').innerText = counts.medium;
        document.getElementById('val-total').innerText = telemetryData.length;

        if (counts.high > 0) {
            const sb = document.getElementById('status-badge');
            sb.innerText = "Intervention Recommended";
            sb.className = "badge badge-high";
        }

        new Chart(document.getElementById('severityChart'), {
            type: 'bar',
            data: {
                labels: ['Info', 'Medium', 'High / Critical'],
                datasets: [{
                    label: 'Event Count',
                    data: [counts.info, counts.medium, counts.high + counts.critical],
                    backgroundColor: ['#1f6feb', '#d29922', '#da3633'],
                    borderRadius: 6
                }]
            },
            options: {
                indexAxis: 'y',
                plugins: { legend: { display: false } },
                scales: { 
                    x: { grid: { color: '#30363d' }, ticks: { color: '#8b949e' } },
                    y: { grid: { display: false }, ticks: { color: '#c9d1d9' } }
                }
            }
        });
    </script>
</body>
</html>
"""

def generate_dashboard(root_dir="."):
    print("     [*] Generating Elite Observability Dashboard...")
    reports_dir = os.path.join(root_dir, "reports")
    db = TelemetryDB(root_dir)
    # Get recent 50 events from DB for a more comprehensive dashboard
    raw_events = db.get_recent_events(50)
    
    # Transform SQL tuples back to JSON-like dicts for JS
    data = []
    for e in raw_events:
        data.append({
            "timestamp": e[0],
            "category": e[1],
            "severity": e[2],
            "source": e[3],
            "message": e[4]
        })
    
    html_content = HTML_TEMPLATE.replace("__TELEMETRY_JSON__", json.dumps(data))
    output_path = os.path.join(reports_dir, "dashboard_elite.html")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"     [+] Dashboard compiled successfully: {output_path}")
    import webbrowser
    webbrowser.open(f"file:///{os.path.abspath(output_path).replace(os.sep, '/')}")

if __name__ == "__main__":
    generate_dashboard(sys.argv[1] if len(sys.argv) > 1 else ".")
