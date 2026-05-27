# PowerTune Desktop UI

This directory contains the React + TypeScript + Tailwind + Tauri workstation UI.

## Purpose
- Provide a desktop-native observability workstation for PowerTune telemetry.
- Offer a high-density, operator-friendly interface for dashboards, correlation timelines, diagnostics, and rollback safety.

## Tech
- React 18 + TypeScript
- Tailwind CSS
- Vite
- Tauri (Rust host)

## Local Development
```powershell
cd desktop
npm.cmd install
npm.cmd run dev
```

Default dev URL: `http://127.0.0.1:1420/`

## Build
```powershell
cd desktop
npm.cmd run build
```

## Tauri
Once you have Rust tooling installed:
```powershell
cd desktop
npm.cmd run tauri dev
```

