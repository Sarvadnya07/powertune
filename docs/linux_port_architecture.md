# Research: PowerTune Linux Port Architecture

## 1. Goal
To bring PowerTune's elite systems observability and controlled optimization to the Linux ecosystem (Phase 96).

## 2. Technical Mapping
The PowerTune architecture is designed to be cross-platform by decoupling the *Core Engine* from the *OS Interface Layer*.

| Windows Component | Linux Equivalent | Role |
| :--- | :--- | :--- |
| **PowerCfg / WMI** | `cpupower` / `tlp` | P-State and C-State configuration. |
| **ETW (Event Tracing)** | `eBPF` / `perf` | Real-time scheduler and interrupt tracking. |
| **nvidia-smi** | `nvidia-smi` (Linux) | GPU residency and P-state tracking. |
| **Win32_Battery** | `upower` / `/sys/class/power_supply/` | Battery health and discharge rate. |
| **ACPI Thermal** | `lm-sensors` / `/sys/class/thermal/` | Thermal saturation monitoring. |

## 3. Implementation Strategy (eBPF)
On Linux, we will leverage **eBPF (Extended Berkeley Packet Filter)** to track CPU wakeups without the overhead of polling. This allows for millisecond-level precision in identifying which background process triggered a core wake-up, far exceeding the capabilities of traditional Linux tools like `powertop`.

## 4. Modular Abstraction
The `core/engine.py` will be updated to include a `LinuxHandler` class, utilizing `subprocess` calls to `systemd` and `sysfs` to enforce power policies identically to the Windows YAML DSL.
