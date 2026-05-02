# Wiki: Modern Standby (S0ix) Forensics

## What is S0ix?
Modern Standby (also known as Connected Standby or S0 Low Power Idle) is the Windows replacement for legacy S3 Sleep. Instead of powering off the RAM, the CPU stays in an ultra-low-power state but remains "connected" to the internet to fetch emails and updates.

## The "Hot Bag" Syndrome
The most common complaint with S0ix is the laptop waking up in a backpack, overheating, and draining the battery to 0% in an hour.

### Root Causes of Standby Wakeups:
1.  **Maintenance Tasks**: Windows decides to run a disk defrag or update scan while "asleep."
2.  **Wake-on-LAN**: A network packet wakes the Wi-Fi card, which in turn wakes the CPU.
3.  **USB Polling**: A mouse dongle or USB-C hub remains active and periodically interrupts the CPU.

## Forensic Analysis with PowerTune
PowerTune's `analyzers/sleep_states.py` uses the **Microsoft-Windows-Power-Troubleshooter** event provider to find the exact "Wake Source."

If your laptop is draining battery while the lid is closed, run the PowerTune `analyze` command to see the forensic history of what exactly triggered the last 5 system wakes.
