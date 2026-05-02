import subprocess
import json
import psutil

class BrowserPowerAnalyzer:
    """
    Phase 8: Research & Intelligence - Browser Power Analysis.
    Correlates browser process activity with timer resolution and CPU usage.
    """
    def __init__(self):
        self.browsers = ["chrome", "msedge", "firefox", "discord", "brave"]

    def get_telemetry(self):
        telemetry = []
        found_browsers = []
        
        # 1. Identify running browser processes
        for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_info']):
            try:
                name = proc.info['name'].lower().split('.')[0]
                if name in self.browsers:
                    found_browsers.append({
                        "name": name,
                        "cpu": proc.info['cpu_percent'],
                        "pid": proc.pid
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if not found_browsers:
            return [{
                "category": "browser_intelligence",
                "severity": "info",
                "source": "system",
                "message": "No intensive browser workloads detected. Idle efficiency is high."
            }]

        # 2. Analyze impact
        for browser in found_browsers:
            if browser['cpu'] > 15:
                telemetry.append({
                    "category": "browser_intelligence",
                    "severity": "medium",
                    "source": browser['name'],
                    "message": f"Browser process (PID {browser['pid']}) is utilizing {browser['cpu']}% CPU. High potential for timer resolution locking."
                })

        # 3. Aggregated Intelligence
        if len(found_browsers) > 5:
            telemetry.append({
                "category": "browser_intelligence",
                "severity": "high",
                "source": "multi-browser",
                "message": f"Detected {len(found_browsers)} active browser processes. Significant risk of C-state exit and cache thrashing."
            })

        return telemetry

if __name__ == "__main__":
    analyzer = BrowserPowerAnalyzer()
    print(json.dumps(analyzer.get_telemetry(), indent=2))
