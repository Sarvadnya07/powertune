import sqlite3
import os
import datetime
import json

class TelemetryDB:
    def __init__(self, root_dir="."):
        self.db_dir = os.path.join(root_dir, "reports", "db")
        os.makedirs(self.db_dir, exist_ok=True)
        self.db_path = os.path.join(self.db_dir, "telemetry_history.db")
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Table for event-based telemetry (anomalies, wakeups, etc)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS telemetry_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    category TEXT,
                    severity TEXT,
                    source TEXT,
                    message TEXT
                )
            """)
            # Table for time-series metrics (battery, cpu, thermal)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metric_name TEXT,
                    value REAL,
                    unit TEXT
                )
            """)
            conn.commit()

    def log_events(self, events):
        """Logs a list of telemetry dictionaries to the events table."""
        if not events:
            return
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for event in events:
                cursor.execute(
                    "INSERT INTO telemetry_events (category, severity, source, message) VALUES (?, ?, ?, ?)",
                    (event.get('category'), event.get('severity'), event.get('source'), event.get('message'))
                )
            conn.commit()

    def log_metric(self, name, value, unit=""):
        """Logs a single numerical metric to the time-series table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO system_metrics (metric_name, value, unit) VALUES (?, ?, ?)",
                (name, value, unit)
            )
            conn.commit()

    def get_recent_metrics(self, metric_name, limit=100):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT timestamp, value FROM system_metrics WHERE metric_name = ? ORDER BY timestamp DESC LIMIT ?",
                (metric_name, limit)
            )
            return cursor.fetchall()

    def get_recent_events(self, limit=10):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT timestamp, category, severity, source, message FROM telemetry_events ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            return cursor.fetchall()

if __name__ == "__main__":
    # Test DB initialization
    db = TelemetryDB()
    db.log_metric("discharge_rate_mw", 4500.5, "mW")
    print(f"Logged test metric to {db.db_path}")
