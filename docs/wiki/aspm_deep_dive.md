# Wiki: PCIe Active State Power Management (ASPM)

## What is ASPM?
Active State Power Management (ASPM) is a power management protocol for PCI Express (PCIe) devices. It allows PCIe links to enter a low-power state when they are not actively transmitting data.

## Why it Matters for Laptops
On high-performance laptops, the PCIe bus (connecting the NVMe SSD, Wi-Fi card, and dGPU) can be a major source of idle power drain if it is kept in an "Active" (L0) state. 

- **L0 State**: Fully active.
- **L0s State**: Low-latency standby.
- **L1 State**: Higher-latency, much lower power standby.

## PowerTune and ASPM
PowerTune's `battery.yaml` profile attempts to force **L1 ASPM** on supported hardware. 

### Common Blockers:
1.  **Vendor Firmware**: Some gaming laptop manufacturers disable ASPM in the BIOS to prevent micro-latencies during gaming.
2.  **External Peripherals**: Many cheap USB-C hubs or external SSDs do not support ASPM correctly, forcing the entire PCIe controller to stay in L0, draining 2W-5W of battery.

## Diagnosis
Use the `analyze` command in PowerTune to identify if the PCIe root complexes are entering deep idle states during system standby.
