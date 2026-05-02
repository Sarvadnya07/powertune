import unittest
import os
import sys
import json

# Ensure we can import from core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.engine import verify_profile_signature, execute_profile
from core.database import TelemetryDB

class TestSafetyEngine(unittest.TestCase):
    def setUp(self):
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.test_profile = os.path.join(self.root_dir, "profiles", "battery.yaml")

    def test_profile_validation(self):
        """Verifies that the cryptographic signature verification logic is functional."""
        self.assertTrue(verify_profile_signature(self.test_profile))

    def test_database_persistence(self):
        """Ensures that the TelemetryDB correctly stores and retrieves events."""
        db = TelemetryDB(self.root_dir)
        test_event = [{"category": "test", "severity": "info", "source": "unit_test", "message": "DB Verification"}]
        db.log_events(test_event)
        
        events = db.get_recent_events(1)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0][1], "test")

    def test_dry_run_safety(self):
        """Ensures that executing a profile in dry-run mode does not crash."""
        try:
            execute_profile(self.test_profile, apply_changes=False, root_dir=self.root_dir)
            success = True
        except Exception as e:
            print(f"Dry-run failed: {e}")
            success = False
        self.assertTrue(success)

if __name__ == "__main__":
    unittest.main()
