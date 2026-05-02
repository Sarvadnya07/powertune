param(
    [switch]$DiagnosticOnly
)

Write-Host "     [*] Running ASUS Module Diagnostics..." -ForegroundColor Yellow

$services = Get-Service | Where-Object Name -match "ArmouryCrate|LightingService|AsusCert"

if ($services) {
    foreach ($svc in $services) {
        if ($svc.Status -eq "Running") {
            Write-Host "     [!] Found ASUS bloat running: $($svc.Name)" -ForegroundColor Red
            if ($svc.Name -match "LightingService") {
                Write-Host "         WHY: LightingService polls RGB controllers aggressively, preventing CPU sleep." -ForegroundColor DarkGray
            }
        } else {
            Write-Host "     [+] ASUS service $($svc.Name) is installed but not running." -ForegroundColor Green
        }
    }
} else {
    Write-Host "     [+] No ASUS bloat services detected." -ForegroundColor Green
}
