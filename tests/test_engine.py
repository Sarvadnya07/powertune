import os
import sys
import pytest

# Add core to sys path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.engine import JsonLogger, BaseTweak, ServiceDisableTweak, SecurityViolationError

def test_json_logger(tmp_path):
    log_dir = tmp_path / "reports"
    logger = JsonLogger(str(log_dir))
    
    logger.log("DisableService", "Success", "Low", "Testing logger")
    
    log_file = log_dir / "changes.log"
    assert log_file.exists()
    
    with open(log_file, "r") as f:
        content = f.read()
        assert "DisableService" in content
        assert "Success" in content

def test_base_tweak():
    data = {
        "risk": "High",
        "why": "Because I said so"
    }
    tweak = BaseTweak(data)
    assert tweak.risk == "High"
    assert tweak.why == "Because I said so"


def test_intent_firewall_blocks_defender():
    # ServiceDisableTweak should raise SecurityViolationError if trying to disable a blocklisted service
    data = {
        "id": "disable_service",
        "target": "windefend",
        "risk": "Critical",
        "why": "Malicious intent"
    }
    
    tweak = ServiceDisableTweak(data)
    with pytest.raises(SecurityViolationError):
        tweak.execute(apply_changes=False)


def test_intent_firewall_allows_safe_service():
    data = {
        "id": "disable_service",
        "target": "LightingService",
        "risk": "Low",
        "why": "RGB bloat"
    }
    
    tweak = ServiceDisableTweak(data)
    assert tweak.target == "LightingService"
