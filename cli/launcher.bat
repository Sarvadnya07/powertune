@echo off
title PowerTune — Laptop Optimization & Diagnostics
color 0B
cls

echo.
echo   =====================================================
echo    PowerTune — Safe Laptop Optimization  Diagnostics
echo   =====================================================
echo.
echo   Choose a command to run:
echo.
echo   [1] Analyze (full diagnostic report)
echo   [2] Battery profile (dry-run)
echo   [3] Battery profile (APPLY — Admin required)
echo   [4] Gaming profile (dry-run)
echo   [5] Gaming profile (APPLY — Admin required)
echo   [6] Developer profile (dry-run)
echo   [7] Silent profile (dry-run)
echo   [8] Vendor detection report
echo   [9] Restore from last snapshot
echo   [0] Exit
echo.
set /p choice="  Enter choice: "

if "%choice%"=="1" powershell.exe -ExecutionPolicy Bypass -File "%~dp0powertune.ps1" analyze
if "%choice%"=="2" powershell.exe -ExecutionPolicy Bypass -File "%~dp0powertune.ps1" battery
if "%choice%"=="3" powershell.exe -ExecutionPolicy Bypass -Verb RunAs -File "%~dp0powertune.ps1" battery -Apply
if "%choice%"=="4" powershell.exe -ExecutionPolicy Bypass -File "%~dp0powertune.ps1" gaming
if "%choice%"=="5" powershell.exe -ExecutionPolicy Bypass -Verb RunAs -File "%~dp0powertune.ps1" gaming -Apply
if "%choice%"=="6" powershell.exe -ExecutionPolicy Bypass -File "%~dp0powertune.ps1" dev
if "%choice%"=="7" powershell.exe -ExecutionPolicy Bypass -File "%~dp0powertune.ps1" silent
if "%choice%"=="8" powershell.exe -ExecutionPolicy Bypass -File "%~dp0powertune.ps1" vendor
if "%choice%"=="9" powershell.exe -ExecutionPolicy Bypass -Verb RunAs -File "%~dp0powertune.ps1" restore -Apply
if "%choice%"=="0" exit

echo.
pause
