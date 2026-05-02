param(
    [switch]$Apply,
    [string]$Vendor,
    [string]$RootDir
)

Write-Host "     [*] Configuring for Stable Thermals (Developer)..." -ForegroundColor Yellow

if ($Apply) {
    & "$RootDir\rollback\snapshot.ps1" -Profile "developer"
    
    powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 98
    powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 98
    powercfg /setactive SCHEME_CURRENT
    
    Write-Host "     [+] Capped CPU Max State to 98%" -ForegroundColor Green
    Write-Host "         WHY: Prevents thermal overshoot and noisy fans during long compiles." -ForegroundColor DarkGray
    
    Write-Host "     [+] Applied Developer Profile successfully." -ForegroundColor Green
} else {
    Write-Host "     [+] (Dry-Run) Would cap CPU Max State to 98%" -ForegroundColor Cyan
    Write-Host "         WHY: Prevents thermal overshoot and noisy fans during long compiles." -ForegroundColor DarkGray
}
