import json

class RootCauseEngine:
    def __init__(self):
        # Heuristic mapping for common issues
        self.rules = {
            "gpu": {
                "high": "The discrete GPU is active despite being idle. This is often caused by browsers (Chrome/Edge) or overlays (Steam/Discord) requesting high-performance rendering.",
            },
            "timers": {
                "medium": "Timer resolution is locked at 1ms. This prevents the CPU from entering deep C-states (C7-C10), increasing package power draw by 1-3 Watts.",
            },
            "power_attribution": {
                "high": "A specific process is saturating a CPU core. If this is a background process, it indicates inefficient task scheduling or a possible memory leak.",
            },
            "anomaly": {
                "high": "Abnormal CPU time detected. This pattern is characteristic of browser-based crypto miners or corrupted telemetry services.",
            },
            "sleep_state": {
                "high": "The system was woken by a peripheral device or a scheduled timer. This indicates 'Modern Standby' is being interrupted by background maintenance tasks.",
            }
        }

    def analyze(self, telemetry_item):
        cat = telemetry_item.get('category', '').lower()
        sev = telemetry_item.get('severity', '').lower()
        
        # Check rule mapping
        if cat in self.rules and sev in self.rules[cat]:
            return self.rules[cat][sev]
        
        return "No specific root-cause analysis available for this event type."

if __name__ == "__main__":
    engine = RootCauseEngine()
    test_event = {"category": "timers", "severity": "medium"}
    print(f"Analysis: {engine.analyze(test_event)}")
