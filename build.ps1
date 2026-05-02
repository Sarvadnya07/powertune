<#
.SYNOPSIS
Builds portable binary executables for the PowerTune Python engines.
.DESCRIPTION
This script uses PyInstaller to compile core/engine.py and core/telemetry.py into standalone .exe files.
This satisfies the "Portable Binary Releases" requirement, allowing users to run PowerTune without installing Python.
#>

$ErrorActionPreference = "Stop"

Write-Host "     [*] Installing build dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

$BuildDir = "build_output"
$BinDir = "bin"

if (-not (Test-Path $BinDir)) { New-Item -ItemType Directory -Path $BinDir | Out-Null }

Write-Host "     [*] Compiling Core Execution Engine..." -ForegroundColor Cyan
pyinstaller --onefile --distpath $BinDir --workpath $BuildDir --name powertune_engine core\engine.py

Write-Host "     [*] Compiling Unified Telemetry Engine..." -ForegroundColor Cyan
pyinstaller --onefile --distpath $BinDir --workpath $BuildDir --name powertune_telemetry core\telemetry.py

Write-Host "     [*] Cleaning up build artifacts..." -ForegroundColor Cyan
Remove-Item -Recurse -Force $BuildDir
Remove-Item -Force *.spec

Write-Host "     [+] Build Complete! Portable binaries are located in the /bin directory." -ForegroundColor Green
