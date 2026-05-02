param(
    [switch]$Apply,
    [string]$SnapshotId,
    [string]$RootDir
)

Write-Host "     [*] System Restore Interface" -ForegroundColor Yellow

$snapshotsDir = Join-Path $RootDir "rollback\snapshots"
if (!(Test-Path $snapshotsDir)) {
    Write-Host "     [!] No snapshots directory found." -ForegroundColor Red
    exit
}

$snapshots = Get-ChildItem -Path $snapshotsDir -Filter "*.json" | Sort-Object LastWriteTime -Descending

if ($snapshots.Count -eq 0) {
    Write-Host "     [!] No snapshots found." -ForegroundColor Red
    exit
}

$target = $snapshots[0]
if ($SnapshotId) {
    $target = $snapshots | Where-Object Name -match $SnapshotId
}

if (-not $target) {
    Write-Host "     [!] Snapshot not found." -ForegroundColor Red
    exit
}

Write-Host "     [+] Found snapshot: $($target.Name)" -ForegroundColor Green

if ($Apply) {
    $data = Get-Content $target.FullName | ConvertFrom-Json
    Write-Host "     [*] Restoring Active Scheme: $($data.ActiveScheme)" -ForegroundColor Yellow
    powercfg /setactive $($data.ActiveScheme)

    if ($null -ne $data.CpuMinAc) {
        Write-Host "     [*] Restoring CPU Min/Max States..." -ForegroundColor Yellow
        powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN $($data.CpuMinAc)
        powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN $($data.CpuMinDc)
        powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX $($data.CpuMaxAc)
        powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX $($data.CpuMaxDc)
        powercfg /setactive SCHEME_CURRENT
    }

    Write-Host "     [+] System state restored successfully." -ForegroundColor Green
} else {
    Write-Host "     [+] (Dry-Run) Would restore snapshot $($target.Name)" -ForegroundColor Cyan
}
