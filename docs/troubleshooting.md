# PowerTune Troubleshooting Guide

## 1. Armoury Crate Causing Battery Drain (ASUS)
**Symptoms**: High CPU usage at idle, frequent dGPU wakeups, and minimum CPU state locked above 5%.
**Diagnosis**: The `LightingService.exe` and `ArmouryCrate.Service.exe` continuously poll the EC (Embedded Controller) over the I2C bus.
**Solution**:
1. Run `.\cli\powertune.ps1 analyze` to verify the WMI drain.
2. Apply the battery profile: `.\cli\powertune.ps1 battery -Apply`. This profile safely disables non-critical RGB polling services while preserving core thermal protections.

## 2. Chrome / Discord Waking the CPU
**Symptoms**: The system idles at 15W instead of 5W, and the fan spins up frequently.
**Diagnosis**: Electron-based apps often request a 1.0ms **Platform Timer Resolution**, preventing the CPU from entering C8 sleep states.
**Solution**:
1. Check the output of the Timers analyzer in PowerTune.
2. If forced to 1ms, disable "Hardware Acceleration" in Discord/Chrome.
3. Restart the browser and re-run the analyzer.

## 3. "Access Denied" during Optimization
**Symptoms**: PowerTune prints a FATAL ERROR and triggers an atomic rollback.
**Diagnosis**: You did not run the PowerShell terminal as an Administrator, or your antivirus blocked the `powercfg` execution.
**Solution**: Open an elevated PowerShell session (`Run as Administrator`) before passing the `-Apply` flag.

## 4. Rollback Failure
**Symptoms**: Running `.\cli\powertune.ps1 restore -Apply` fails to revert the CPU max state.
**Diagnosis**: The JSON snapshot may have been corrupted or manually edited.
**Solution**: Manually open the Windows Control Panel -> Power Options -> Change plan settings -> Change advanced power settings, and manually reset Processor Power Management.
