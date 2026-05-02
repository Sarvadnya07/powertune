<#
.SYNOPSIS
PowerTune Professional Installer
.DESCRIPTION
Automates environment setup, dependency installation, and PATH configuration.
#>

$ErrorActionPreference = "Stop"

Write-Host "  =====================================================" -ForegroundColor Cyan
Write-Host "   PowerTune — Platform Installation & Setup" -ForegroundColor Cyan
Write-Host "  =====================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check for Admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "  [!] NOTICE: Installer is not running as Administrator." -ForegroundColor Yellow
    Write-Host "      Some PATH modifications and service optimizations may be restricted." -ForegroundColor Gray
}

# 2. Check for Python
Write-Host "  [*] Checking for Python..." -ForegroundColor White
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Host "  [!] ERROR: Python not found. Please install Python 3.10+ and try again." -ForegroundColor Red
    exit 1
}
Write-Host "      Found: $($py.Source)" -ForegroundColor Gray

# 3. Setup Virtual Environment
Write-Host "  [*] Setting up Python virtual environment (.venv)..." -ForegroundColor White
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

# Use the venv's python/pip
$venvPath = Join-Path $PSScriptRoot ".venv"
$pip = Join-Path $venvPath "Scripts\pip.exe"

Write-Host "  [*] Installing Python dependencies in venv..." -ForegroundColor White
& $pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "      Dependencies installed successfully in .venv." -ForegroundColor Green
} else {
    Write-Host "      Failed to install dependencies." -ForegroundColor Red
    exit 1
}

# 4. PATH Configuration
Write-Host ""
$choice = Read-Host "  [?] Would you like to add PowerTune to your User PATH? (y/n)"
if ($choice -eq 'y') {
    $cliPath = Join-Path $PSScriptRoot "cli"
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    
    if ($currentPath -split ";" -contains $cliPath) {
        Write-Host "      PowerTune is already in your PATH." -ForegroundColor Green
    } else {
        Write-Host "      Adding $cliPath to User PATH..." -ForegroundColor White
        [Environment]::SetEnvironmentVariable("Path", $currentPath + ";" + $cliPath, "User")
        Write-Host "      Success! Restart your terminal to use 'powertune' globally." -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "  [+] Installation Complete. You are ready to optimize." -ForegroundColor Green
Write-Host "      Try running: powertune analyze" -ForegroundColor Gray
Write-Host ""
