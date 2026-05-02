param(
    [switch]$Apply,
    [string]$Vendor,
    [string]$RootDir
)

Write-Host "     [*] Configuring for Maximum FPS & Minimum Latency..." -ForegroundColor Yellow

if ($Apply) {
    & "$RootDir\rollback\snapshot.ps1" -Profile "gaming"
    
    # Set to High Performance (GUID: 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c)
    powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
    
    Write-Host "     [+] Switched to High Performance Scheme" -ForegroundColor Green
    Write-Host "         WHY: Prevents CPU downclocking during game loads." -ForegroundColor DarkGray
    
    Write-Host "     [+] Applied Gaming Profile successfully." -ForegroundColor Green
} else {
    Write-Host "     [+] (Dry-Run) Would switch to High Performance power scheme" -ForegroundColor Cyan
    Write-Host "         WHY: Prevents CPU downclocking during game loads." -ForegroundColor DarkGray
}
