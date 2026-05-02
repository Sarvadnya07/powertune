param(
    [switch]$Apply,
    [string]$Vendor,
    [string]$RootDir
)

Write-Host "     [*] Configuring for Maximum Battery Life..." -ForegroundColor Yellow

if ($Apply) {
    # Call Snapshot
    & "$RootDir\rollback\snapshot.ps1" -Profile "battery"
    
    # Apply settings
    powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 5
    powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 5
    powercfg /setactive SCHEME_CURRENT
    
    Write-Host "     [+] Lowered CPU Minimum State to 5%" -ForegroundColor Green
    Write-Host "         WHY: Allows processor to enter deeper C-states when idle." -ForegroundColor DarkGray
    
    Write-Host "     [+] Applied Battery Profile successfully." -ForegroundColor Green
} else {
    Write-Host "     [+] (Dry-Run) Would lower CPU Minimum State to 5%" -ForegroundColor Cyan
    Write-Host "         WHY: Allows processor to enter deeper C-states when idle." -ForegroundColor DarkGray
}
