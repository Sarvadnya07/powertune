import json
from core.database import TelemetryDB

class PredictiveEngine:
    """
    Phase 9: AI & Future Intelligence - Predictive Analytics.
    Analyzes historical TelemetryDB trends to predict degradation and anomalies.
    """
    def __init__(self, root_dir="."):
        self.db = TelemetryDB(root_dir)

    def predict_battery_health(self):
        """Analyzes discharge trends to predict battery health decline."""
        metrics = self.db.get_recent_metrics("discharge_rate_mw", limit=50)
        if len(metrics) < 10:
            return "Insufficient historical data for accurate battery prediction."
            
        values = [m[1] for m in metrics]
        avg_drain = sum(values) / len(values)
        
        if avg_drain > 15000:
            return "WARNING: Sustained high discharge rate detected (>15W). Predicted battery cycle life may decline by 20% faster than average."
        return "Battery discharge trends are within optimal parameters for long-term health."

    def detect_thermal_anomalies(self):
        """Analyzes thermal telemetry to predict cooling efficiency decline."""
        events = self.db.get_recent_events(limit=50)
        thermal_alerts = [e for e in events if e[1] == 'thermal' and e[2] in ['medium', 'high']]
        
        if len(thermal_alerts) > 5:
            return "ANOMALY: Recurring thermal throttling detected. Predicted cooling efficiency has declined. Internal fan cleaning or repasting may be required."
        return "Thermal regulation is stable."

    def get_recommendations(self):
        return {
            "battery_prediction": self.predict_battery_health(),
            "thermal_prediction": self.detect_thermal_anomalies()
        }

if __name__ == "__main__":
    engine = PredictiveEngine()
    print(json.dumps(engine.get_recommendations(), indent=2))
