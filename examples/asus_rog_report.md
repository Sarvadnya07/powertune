# PowerTune Diagnostic Report: ASUS ROG Zephyrus

**Date**: 2026-05-02
**System**: ASUS ROG Zephyrus G14
**OS**: Windows 11 Pro (22631)

## 1. Battery Health
- **Design Capacity**: 76,000 mWh
- **Full Charge Capacity**: 64,500 mWh
- **Wear Level**: 15.1%
- **Status**: [OK] Battery health is acceptable.

## 2. GPU Residency
- **dGPU State**: ACTIVE (Waking)
- **Processes keeping NVIDIA GPU awake**:
  - `Discord.exe` (Hardware Acceleration enabled)
  - `EpicGamesLauncher.exe`
- **Impact**: System drawing ~18W at idle instead of ~6W.

## 3. Vendor Bloat Services
- Detected `ASUS System Control Interface`.
- `LightingService.exe` is consuming 2% CPU at idle to poll RGB states.

## 4. Resolution
Applying `profiles/battery.yaml` successfully capped CPU max state, disabled `LightingService`, and forced dGPU to P8 Sleep State.

**Post-Optimization Idle Power**: 7.2W
