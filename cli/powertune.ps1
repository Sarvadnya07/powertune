<#
.SYNOPSIS
    PowerTune — Cross-vendor laptop optimization & diagnostics CLI dispatcher.

.DESCRIPTION
    The main entry point for PowerTune. Handles sub-command routing, vendor detection,
    admin privilege checking, and dry-run safety enforcement.

    Usage:
        .\cli\powertune.ps1 analyze
        .\cli\powertune.ps1 battery [-Apply]
        .\cli\powertune.ps1 gaming  [-Apply]
        .\cli\powertune.ps1 dev     [-Apply]
        .\cli\powertune.ps1 silent  [-Apply]
        .\cli\powertune.ps1 vendor
        .\cli\powertune.ps1 restore [-SnapshotId <id>]
        .\cli\powertune.ps1 help

.PARAMETER Command
    The sub-command to execute.

.PARAMETER Apply
    If specified, changes are actually applied. Default is dry-run (safe).

.PARAMETER SnapshotId
    For the 'restore' command, specifies which snapshot to restore from.
    If omitted, the most recent snapshot is used.
#>

param(
    [Parameter(Position=0)]
    [ValidateSet("analyze", "benchmark", "battery", "gaming", "dev", "silent", "vendor", "restore", "help", "")]
    [string]$Command = "help",

    [switch]$Apply,

    [string]$SnapshotId = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ─── Paths ────────────────────────────────────────────────────────────────────
$Root        = Split-Path $PSScriptRoot -Parent
$ProfilesDir = Join-Path $Root "profiles"
$VendorDir   = Join-Path $Root "vendor"
$RollbackDir = Join-Path $Root "rollback"
$AnalyzersDir= Join-Path $Root "analyzers"
$ReportsDir  = Join-Path $Root "reports"

# Ensure reports directory exists
if (!(Test-Path $ReportsDir)) { New-Item -ItemType Directory -Path $ReportsDir | Out-Null }

# ─── Helpers ──────────────────────────────────────────────────────────────────
function Write-Banner {
    Clear-Host
    Write-Host ""
    Write-Host "  ██████╗  ██████╗ ██╗    ██╗███████╗██████╗ ████████╗██╗   ██╗███╗   ██╗███████╗" -ForegroundColor Cyan
    Write-Host "  ██╔══██╗██╔═══██╗██║    ██║██╔════╝██╔══██╗╚══██╔══╝██║   ██║████╗  ██║██╔════╝" -ForegroundColor Cyan
    Write-Host "  ██████╔╝██║   ██║██║ █╗ ██║█████╗  ██████╔╝   ██║   ██║   ██║██╔██╗ ██║█████╗  " -ForegroundColor Cyan
    Write-Host "  ██╔═══╝ ██║   ██║██║███╗██║██╔══╝  ██╔══██╗   ██║   ██║   ██║██║╚██╗██║██╔══╝  " -ForegroundColor Cyan
    Write-Host "  ██║     ╚██████╔╝╚███╔███╔╝███████╗██║  ██║   ██║   ╚██████╔╝██║ ╚████║███████╗" -ForegroundColor Cyan
    Write-Host "  ╚═╝      ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚══════╝" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Safe, explainable, reversible laptop optimization & diagnostics." -ForegroundColor Gray
    Write-Host "  v1.0.0  |  MIT License  |  https://github.com/you/powertune" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  ─────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray
    Write-Host ""
}

function Write-Header([string]$Text) {
    Write-Host "  🔹 $Text" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Working([string]$Text) {
    Write-Host "     [*] $Text" -ForegroundColor Yellow
}

function Write-Success([string]$Text) {
    Write-Host "     [+] $Text" -ForegroundColor Green
}

function Write-Info([string]$Text) {
    Write-Host "     [i] $Text" -ForegroundColor Gray
}

function Write-Why([string]$Text) {
    Write-Host "         WHY: $Text" -ForegroundColor DarkGray
}

function Write-Warn([string]$Text) {
    Write-Host "     [!] $Text" -ForegroundColor Red
}

function Write-DryRun {
    Write-Host ""
    Write-Host "  ┌─────────────────────────────────────────────────────────────┐" -ForegroundColor DarkYellow
    Write-Host "  │  DRY-RUN MODE — No changes have been made to your system.   │" -ForegroundColor DarkYellow
    Write-Host "  │  Re-run with -Apply (as Administrator) to commit changes.   │" -ForegroundColor DarkYellow
    Write-Host "  └─────────────────────────────────────────────────────────────┘" -ForegroundColor DarkYellow
    Write-Host ""
}

function Test-Admin {
    return ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
        [Security.Principal.WindowsBuiltInRole]::Administrator
    )
}

function Get-Vendor {
    $manufacturer = (Get-CimInstance -ClassName Win32_ComputerSystem -ErrorAction SilentlyContinue).Manufacturer
    if ($manufacturer -match "ASUS|ASUSTeK") { return "asus" }
    if ($manufacturer -match "LENOVO")        { return "lenovo" }
    if ($manufacturer -match "DELL")          { return "dell" }
    if ($manufacturer -match "HP|HEWLETT")    { return "hp" }
    return "unknown"
}

function Get-PythonCommand {
    $venvPy = Join-Path $Root ".venv\Scripts\python.exe"
    if (Test-Path $venvPy) { return $venvPy }
    return "python"
}

function Test-Python {
    $pyCmd = Get-PythonCommand
    $py = Get-Command $pyCmd -ErrorAction SilentlyContinue
    if (-not $py) {
        Write-Warn "Python not found in PATH or .venv. Analyzer features require Python 3.10+."
        Write-Info "Run .\install.ps1 to set up the environment automatically."
        return $false
    }
    return $true
}

# ─── Command: help ────────────────────────────────────────────────────────────
function Invoke-Help {
    Write-Host "  USAGE:" -ForegroundColor White
    Write-Host "    .\cli\powertune.ps1 <command> [-Apply] [-SnapshotId <id>]"
    Write-Host ""
    Write-Host "  COMMANDS:" -ForegroundColor White

    $cmds = @(
        @{ Cmd="analyze"; Desc="Run full diagnostic suite (battery, CPU, timers, services)" }
        @{ Cmd="benchmark"; Desc="Scientific measurement of idle power & efficiency" }
        @{ Cmd="dashboard"; Desc="Generate and launch the interactive web dashboard" }
        @{ Cmd="battery "; Desc="Apply battery-saver optimization profile" }
        @{ Cmd="gaming  "; Desc="Apply gaming performance profile" }
        @{ Cmd="dev     "; Desc="Apply developer thermal-balanced profile" }
        @{ Cmd="silent  "; Desc="Apply silent / minimum-fan profile" }
        @{ Cmd="vendor  "; Desc="Detect vendor software and report bloat services" }
        @{ Cmd="restore "; Desc="Revert system to a previous PowerTune snapshot" }
        @{ Cmd="help    "; Desc="Show this help message" }
    )

    foreach ($c in $cmds) {
        Write-Host ("    {0,-10}  {1}" -f $c.Cmd, $c.Desc) -ForegroundColor Gray
    }

    Write-Host ""
    Write-Host "  FLAGS:" -ForegroundColor White
    Write-Host "    -Apply           Commit changes (requires Administrator). Default is dry-run." -ForegroundColor Gray
    Write-Host "    -SnapshotId <id> Restore a specific snapshot (use with 'restore' command)." -ForegroundColor Gray
    Write-Host ""
    Write-Host "  EXAMPLES:" -ForegroundColor White
    Write-Host "    .\cli\powertune.ps1 analyze" -ForegroundColor DarkCyan
    Write-Host "    .\cli\powertune.ps1 battery" -ForegroundColor DarkCyan
    Write-Host "    .\cli\powertune.ps1 battery -Apply   # (Run as Administrator)" -ForegroundColor DarkCyan
    Write-Host "    .\cli\powertune.ps1 restore" -ForegroundColor DarkCyan
    Write-Host ""
}

# ─── Command: analyze ─────────────────────────────────────────────────────────
function Invoke-Analyze {
    Write-Header "Diagnostic Analyzer"

    $vendor = Get-Vendor
    Write-Working "Detected vendor: $($vendor.ToUpper())"
    Write-Why "Vendor detection tailors diagnostic checks to known bloat services for your OEM."
    Write-Host ""

    if (Test-Python) {
        $py = Get-PythonCommand
        Write-Working "Running battery analyzer..."
        $batteryOut = & $py "$AnalyzersDir\battery.py" --report-dir "$ReportsDir" 2>&1
        $batteryOut | ForEach-Object { Write-Host "     $_" -ForegroundColor Gray }
        Write-Host ""

        Write-Working "Running CPU analyzer..."
        $cpuOut = & $py "$AnalyzersDir\cpu.py" 2>&1
        $cpuOut | ForEach-Object { Write-Host "     $_" -ForegroundColor Gray }
        Write-Host ""

        Write-Working "Running services analyzer..."
        $svcOut = & $py "$AnalyzersDir\services.py" 2>&1
        $svcOut | ForEach-Object { Write-Host "     $_" -ForegroundColor Gray }
        Write-Host ""

        Write-Working "Running GPU analyzer..."
        $gpuOut = & $py "$AnalyzersDir\gpu_residency.py" 2>&1
        $gpuOut | ForEach-Object { Write-Host "     $_" -ForegroundColor Gray }
        Write-Host ""

        Write-Working "Running dependencies analyzer..."
        $depsOut = & $py "$AnalyzersDir\dependencies.py" 2>&1
        $depsOut | ForEach-Object { Write-Host "     $_" -ForegroundColor Gray }
        Write-Host ""

        Write-Host "  ─────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray
        Write-Working "Running Advanced AI Telemetry & Recommendation Engine..."
        $telOut = & $py "$Root\core\telemetry.py" "$Root" 2>&1
        $telOut | ForEach-Object { Write-Host "     $_" -ForegroundColor Cyan }
        Write-Host ""
    } else {
        Write-Warn "Skipping Python analyzers — Python not available."
        Write-Info "Running PowerShell-only diagnostics..."
        Write-Host ""

        $scheme = powercfg /getactivescheme
        Write-Working "Active Power Scheme:"
        Write-Info $scheme
        Write-Host ""
    }

    # Run vendor-specific scan non-destructively
    Write-Working "Running vendor diagnostic: $($vendor.ToUpper())..."
    $vendorScript = Join-Path $VendorDir "$vendor.ps1"
    if (Test-Path $vendorScript) {
        & $vendorScript -DiagnosticOnly
    } else {
        Write-Info "No specific vendor module for '$vendor'. Skipping vendor scan."
    }
    Write-Host ""

    if (-not (Test-Admin)) {
        Write-Info "Tip: Run as Administrator for a deeper energy trace (powercfg /energy)."
    }
}

# ─── Command: benchmark ───────────────────────────────────────────────────────
function Invoke-Benchmark {
    Write-Header "Performance & Efficiency Benchmark"
    if (Test-Python) {
        $py = Get-PythonCommand
        & $py "$Root\core\benchmark.py"
    } else {
        Write-Warn "Python is required for benchmarking."
    }
}

# ─── Command: profile dispatcher ──────────────────────────────────────────────
function Invoke-Profile([string]$ProfileName) {
    Write-Header "$ProfileName Profile"

    if ($Apply -and -not (Test-Admin)) {
        Write-Warn "-Apply requires Administrator privileges."
        Write-Info "Right-click powertune.ps1 → Run as Administrator, then re-run with -Apply."
        exit 1
    }

    if (-not $Apply) { Write-DryRun }

    $yamlPath = Join-Path $ProfilesDir "$ProfileName.yaml"
    if (Test-Path $yamlPath) {
        Write-Working "Using YAML Configuration Engine..."
        $argsList = @($yamlPath, "--root", $Root)
        if ($Apply) { $argsList += "--apply" }
        $py = Get-PythonCommand
        & $py "$Root\core\engine.py" @argsList
    } else {
        $script = Join-Path $ProfilesDir "$ProfileName.ps1"
        if (!(Test-Path $script)) {
            Write-Warn "Profile script/yaml not found: $ProfileName"
            exit 1
        }
        & $script -Apply:$Apply -Vendor (Detect-Vendor) -RootDir $Root
    }
}

# ─── Command: vendor ──────────────────────────────────────────────────────────
function Invoke-Vendor {
    Write-Header "Vendor Detection & Bloat Report"
    $vendor = Detect-Vendor
    Write-Working "Detected: $($vendor.ToUpper())"
    Write-Host ""

    $vendorScript = Join-Path $VendorDir "$vendor.ps1"
    if (Test-Path $vendorScript) {
        & $vendorScript -DiagnosticOnly
    } else {
        Write-Info "No vendor module for '$vendor'. Supported: asus, lenovo, dell, hp."
    }
}

# ─── Command: restore ─────────────────────────────────────────────────────────
function Invoke-Restore {
    Write-Header "System Restore"

    if ($Apply -and -not (Test-Admin)) {
        Write-Warn "-Apply requires Administrator privileges for restore operations."
        exit 1
    }

    if (-not $Apply) { Write-DryRun }

    $restoreScript = Join-Path $RollbackDir "restore.ps1"
    & $restoreScript -Apply:$Apply -SnapshotId $SnapshotId -RootDir $Root
}

# ─── Command: dashboard ───────────────────────────────────────────────────────
function Invoke-Dashboard {
    Write-Header "Interactive Observability Dashboard"
    if (Test-Python) {
        $py = Get-PythonCommand
        & $py "$Root\core\dashboard.py" "$Root"
    } else {
        Write-Warn "Python is required to generate the dashboard."
    }
}

# ─── Main ─────────────────────────────────────────────────────────────────────
Write-Banner

try {
    switch ($Command) {
        "analyze" { Invoke-Analyze }
        "benchmark" { Invoke-Benchmark }
        "dashboard" { Invoke-Dashboard }
        "battery" { Invoke-Profile "battery" }
        "gaming"  { Invoke-Profile "gaming" }
        "dev"     { Invoke-Profile "developer" }
        "silent"  { Invoke-Profile "silent" }
        "vendor"  { Invoke-Vendor }
        "restore" { Invoke-Restore }
        "help"    { Invoke-Help }
        default   { Invoke-Help }
    }
} catch {
    Write-Warn "FATAL ERROR: $($_.Exception.Message)"
    Write-Info "Please check reports/changes.log for details or report this issue on GitHub."
    exit 1
}

Write-Host ""
Write-Host "  ─────────────────────────────────────────────────────────────────" -ForegroundColor DarkGray
Write-Host "  PowerTune | All changes are logged to reports/changes.log" -ForegroundColor DarkGray
Write-Host ""
