import subprocess
import json
import time
import sys
import os

class BenchmarkResult:
    def __init__(self):
        self.avg_cpu_usage = 0
        self.avg_cpu_freq = 0
        self.discharge_rate_mw = 0
        self.process_count = 0
        self.timestamp = time.time()

def get_process_count():
    try:
        out = subprocess.check_output(["powershell", "-Command", "(Get-Process).Count"], text=True, timeout=5.0).strip()
        return int(out)
    except:
        return 0

def get_cpu_stats():
    try:
        # Get Average CPU usage and Frequency
        ps_script = """
        $usage = (Get-CimInstance -ClassName Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average
        $freq = (Get-CimInstance -ClassName Win32_Processor).CurrentClockSpeed
        "$usage|$freq"
        """
        out = subprocess.check_output(["powershell", "-Command", ps_script], text=True, timeout=10.0).strip()
        usage, freq = out.split('|')
        return float(usage), int(freq)
    except:
        return 0.0, 0

def get_battery_discharge_rate():
    try:
        # MsAcpi_BatteryStatus provides DischargeRate in mW
        ps_script = """
        Get-CimInstance -Namespace root/wmi -ClassName MsAcpi_BatteryStatus | 
        Select-Object DischargeRate | ConvertTo-Json
        """
        out = subprocess.check_output(["powershell", "-Command", ps_script], text=True, timeout=5.0).strip()
        if out:
            data = json.loads(out)
            return data.get("DischargeRate", 0)
    except:
        pass
    return 0

def run_advanced_benchmark(duration_sec=30):
    print(f"     [*] Initiating Scientific Benchmark ({duration_sec}s idle period)...")
    print("     [*] RECOMMENDATION: Close all applications and remain idle for accuracy.")
    
    samples = []
    start_time = time.time()
    
    while time.time() - start_time < duration_sec:
        usage, freq = get_cpu_stats()
        rate = get_battery_discharge_rate()
        proc_count = get_process_count()
        
        samples.append({
            "usage": usage,
            "freq": freq,
            "rate": rate,
            "procs": proc_count
        })
        time.sleep(5)
        print(f"     [*] Sampling... ({int(time.time() - start_time)}s / {duration_sec}s)")

    if not samples:
        return None

    avg_usage = sum(s['usage'] for s in samples) / len(samples)
    avg_freq = sum(s['freq'] for s in samples) / len(samples)
    avg_rate = sum(s['rate'] for s in samples) / len(samples)
    final_procs = samples[-1]['procs']

    result = {
        "avg_cpu_usage_percent": round(avg_usage, 2),
        "avg_cpu_frequency_mhz": round(avg_freq, 0),
        "avg_discharge_rate_mw": round(avg_rate, 0),
        "process_count": final_procs,
        "score": round(10000 / (avg_usage + 1) * (1 / (avg_freq + 1)) * 10, 0) # Pseudo-efficiency score
    }

    return result

if __name__ == "__main__":
    res = run_advanced_benchmark(15) # Shorter for testing
    if res:
        print("\n     [+] BENCHMARK COMPLETE")
        print(f"         Average CPU Usage: {res['avg_cpu_usage_percent']}%")
        print(f"         Average CPU Freq:  {res['avg_cpu_frequency_mhz']} MHz")
        if res['avg_discharge_rate_mw'] > 0:
            print(f"         Discharge Rate:    {res['avg_discharge_rate_mw']} mW")
        print(f"         Process Count:     {res['process_count']}")
        print(f"         Efficiency Score:  {res['score']}")
