import os
import sys
import json
import subprocess
from datetime import datetime
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

def run_battery_report(output_path):
    print("     [*] Generating powercfg /batteryreport...")
    try:
        subprocess.run(["powercfg", "/batteryreport", "/output", output_path], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def parse_report(file_path):
    if not BeautifulSoup:
        return {"status": "warning", "message": "BeautifulSoup4 not installed.", "why": "Run 'pip install beautifulsoup4 lxml' for advanced HTML parsing.", "recommendation": "Install dependencies for full diagnostic capability."}
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'lxml')
    # Basic mock parsing for MVP
    # Finding design capacity and full charge capacity
    design_cap = "Unknown"
    full_cap = "Unknown"
    
    tables = soup.find_all('table')
    for table in tables:
        text = table.text.upper()
        if "DESIGN CAPACITY" in text and "FULL CHARGE CAPACITY" in text:
            rows = table.find_all('tr')
            for row in rows:
                if "DESIGN CAPACITY" in row.text.upper():
                    cols = row.find_all('td')
                    if len(cols) > 1: design_cap = cols[1].text.strip()
                if "FULL CHARGE CAPACITY" in row.text.upper():
                    cols = row.find_all('td')
                    if len(cols) > 1: full_cap = cols[1].text.strip()
            break
            
    if design_cap != "Unknown" and full_cap != "Unknown":
        try:
            d = int(''.join(filter(str.isdigit, design_cap)))
            f = int(''.join(filter(str.isdigit, full_cap)))
            wear = 100 - (f / d * 100)
            return {
                "status": "warning" if wear > 20 else "ok",
                "message": f"Battery Wear Level: {wear:.1f}%",
                "why": f"Design: {d} mWh, Current Max: {f} mWh.",
                "recommendation": "Battery health is acceptable." if wear <= 20 else "Consider replacing battery or capping charge limit."
            }
        except:
            pass

    return {"status": "ok", "message": "Battery Report Parsed", "why": "Unable to extract exact wear numbers.", "recommendation": "Check report manually."}

if __name__ == "__main__":
    report_dir = sys.argv[sys.argv.index('--report-dir')+1] if '--report-dir' in sys.argv else "."
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, "battery_report.html")
    
    if run_battery_report(report_path):
        result = parse_report(report_path)
        print(f"     [{'+' if result['status'] == 'ok' else '!'}] {result['message']}")
        print(f"         WHY: {result['why']}")
        if result['recommendation']:
            print(f"         REC: {result['recommendation']}")
    else:
        print("     [!] Failed to generate battery report.")
