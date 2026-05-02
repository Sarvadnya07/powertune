"""
PowerTune Power Attribution Model (v1.0)
Mathematically estimating per-process energy consumption on Windows.
"""

class PowerModel:
    def __init__(self, tdp_watts=15, battery_capacity_mwh=50000):
        self.tdp_watts = tdp_watts
        self.battery_capacity_mwh = battery_capacity_mwh

    def estimate_process_impact(self, cpu_percent_time, has_gpu_handle=False, is_timer_offender=False):
        """
        Calculates estimated hourly battery drain contribution (in mWh).
        
        Logic:
        - Base CPU impact: (CPU% / 100) * TDP * ActivityFactor
        - GPU Wakeup Penalty: +5W baseline if active
        - Timer Penalty: +2W if forcing 1ms resolution
        """
        
        # 1. CPU Component
        # Modern mobile CPUs draw roughly 10% of TDP at 5% load due to clock ramp
        cpu_wattage = (cpu_percent_time / 100.0) * self.tdp_watts * 1.5
        
        # 2. Discrete GPU Wakeup Penalty
        # If a process wakes the dGPU, it incurs the entire dGPU idle floor (~5W-8W)
        gpu_penalty = 6.5 if has_gpu_handle else 0.0
        
        # 3. Platform Timer Penalty
        # Forcing 1ms timer prevents deep C-states, adding ~1.5W baseline drain
        timer_penalty = 1.5 if is_timer_offender else 0.0
        
        total_wattage = cpu_wattage + gpu_penalty + timer_penalty
        
        # Return estimated percentage of total battery life consumed per hour
        battery_life_impact_percent = (total_wattage / (self.battery_capacity_mwh / 1000.0)) * 100
        
        return {
            "estimated_wattage": round(total_wattage, 2),
            "battery_impact_percent": round(battery_life_impact_percent, 2),
            "severity": "high" if total_wattage > 3.0 else "medium" if total_wattage > 1.0 else "info"
        }

# Example Usage:
# model = PowerModel(tdp_watts=28)
# impact = model.estimate_process_impact(cpu_percent_time=12, has_gpu_handle=True)
# print(f"This process is draining {impact['estimated_wattage']}W from your battery.")
