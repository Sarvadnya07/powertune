# Power Optimization Theory

This document outlines the core scientific principles that drive the PowerTune Systems Observability Platform. Understanding these concepts is critical before contributing new optimization profiles.

## 1. CPU Residency & C-States
Modern CPUs save power by entering idle states known as **C-States** (e.g., C0 is active, C8 is deep sleep). 
The goal of PowerTune is not necessarily to "underclock" the CPU, but to maximize the time the CPU spends in deep C-States.
- **Interrupt Storms**: A poorly written background service (like vendor RGB software) might poll the system every 5 milliseconds. This prevents the CPU from ever entering C8, drawing 15W at idle instead of 3W.

## 2. Platform Timer Resolution
Windows uses a system timer to schedule thread execution. The default resolution is **15.6ms**.
- Certain applications (like Chrome, Discord, or older games) aggressively request a **1.0ms** or **0.5ms** timer resolution.
- This forces the CPU to wake up 1,000 times per second, destroying battery life. PowerTune tracks this via `analyzers/timers.py`.

## 3. GPU Residency & Wakeups
A discrete GPU (dGPU) like an NVIDIA RTX chip should be in a deep sleep state (P8) when not gaming.
- If an electron app (e.g., Epic Games Launcher) utilizes hardware acceleration, it will wake the dGPU. 
- Waking the dGPU instantly adds 10W-20W to the baseline power draw. PowerTune uses `nvidia-smi` to catch these rogue processes.

## 4. Modern Standby (S0ix) vs S3 Sleep
Modern Windows laptops utilize S0ix (Connected Standby), meaning the CPU operates in a very low power state but does not fully power off the RAM like legacy S3 sleep.
- Wake triggers (like an aggressive Wi-Fi packet or a USB hub polling) can wake the system from S0ix while the lid is closed, resulting in the infamous "laptop is burning hot in my backpack" issue. PowerTune tracks these wake events via `analyzers/sleep_states.py`.
