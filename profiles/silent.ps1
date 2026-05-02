param(
    [switch]$Apply,
    [string]$Vendor,
    [string]$RootDir
)

Write-Host "     [*] Configuring for Minimum Fan Noise..." -ForegroundColor Yellow

if ($Apply) {
    & "$RootDir\rollback\snapshot.ps1" -Profile "silent"
    
    powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 70
    powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 70
    powercfg /setactive SCHEME_CURRENT
    
    Write-Host "     [+] Capped CPU Max State to 70%" -ForegroundColor Green
    Write-Host "         WHY: Forces CPU to stay cool, preventing fans from spinning up." -ForegroundColor DarkGray
    
    Write-Host "     [+] Applied Silent Profile successfully." -ForegroundColor Green
} else {
    Write-Host "     [+] (Dry-Run) Would cap CPU Max State to 70%" -ForegroundColor Cyan
    Write-Host "         WHY: Forces CPU to stay cool, preventing fans from spinning up." -ForegroundColor DarkGray
}
