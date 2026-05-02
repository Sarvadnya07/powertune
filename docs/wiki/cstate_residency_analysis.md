# Wiki: CPU C-State Residency Analysis

## Understanding Idle States
CPUs do not just "turn off." Instead, they transition through various **C-States** (Idle States).

| State | Name | Description |
| :--- | :--- | :--- |
| **C0** | Operating | CPU is actively executing instructions. |
| **C1** | Halt | Clock is stopped. |
| **C6** | Deep Sleep | Core voltage is significantly reduced. |
| **C8-C10** | Ultra Deep Sleep | Essential for modern laptop battery life (S0ix). |

## The Problem: Background Noise
A CPU cannot enter a deep C8 state if there is any "noise" on the system. Noise is defined as any interrupt or scheduled thread that wakes a core.

### Common Sources of Noise:
1.  **High Timer Resolution**: If an app (like Discord) forces a 1ms timer, the CPU is forced out of sleep 1,000 times every second.
2.  **Frequent WMI Polling**: Vendor software (like ASUS Armoury Crate) often polls hardware temperatures every 100ms. This prevents the package from ever entering C10.

## How PowerTune Helps
PowerTune's `analyzers/cpu.py` and `analyzers/timers.py` modules quantify your **Residency Percentage**. 

For elite-level battery life, your goal is **>90% Residency in C8+** at idle. If you are stuck at 40% residency, your battery life will be cut in half regardless of your "Battery Saver" settings.
