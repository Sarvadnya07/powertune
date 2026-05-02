import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from analyzers.battery import parse_report

def test_battery_parse():
    mock_html = """
    <html><body>
    <table>
        <tr><td>DESIGN CAPACITY</td><td>50,000 mWh</td></tr>
        <tr><td>FULL CHARGE CAPACITY</td><td>45,000 mWh</td></tr>
    </table>
    </body></html>
    """
    
    test_file = "test_battery.html"
    with open(test_file, "w") as f:
        f.write(mock_html)
        
    try:
        res = parse_report(test_file)
        assert res['status'] in ['ok', 'warning']
        print("[+] parse_report handles mock html successfully")
    finally:
        os.remove(test_file)

if __name__ == "__main__":
    test_battery_parse()
