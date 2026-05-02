param(
    [switch]$DiagnosticOnly
)

Write-Host "     [*] Lenovo Vendor Module: Scanning for Vantage Telemetry & Bloat" -ForegroundColor Gray

$lenovoServices = @(
    "ImControllerService", # Lenovo System Interface Foundation
    "LenovoVantageService",
    "YMC"                  # Yoga Mode Control (often causes high CPU)
)

$found = 0
foreach ($svc in $lenovoServices) {
    $status = Get-Service -Name $svc -ErrorAction SilentlyContinue
    if ($status -and $status.Status -eq 'Running') {
        Write-Host "     [!] Detected active Lenovo telemetry service: $svc" -ForegroundColor Yellow
        $found++
    }
}

if ($found -eq 0) {
    Write-Host "     [+] Lenovo ecosystem is clean. No active telemetry services found." -ForegroundColor Green
} else {
    Write-Host "         WHY: Lenovo Vantage background services are known to poll WMI frequently, preventing C8 sleep." -ForegroundColor Gray
}
