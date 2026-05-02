param(
    [switch]$DiagnosticOnly
)

Write-Host "     [*] HP Vendor Module: Scanning for OMEN Hub & Support Assistant" -ForegroundColor Gray

$hpServices = @(
    "HPSupportSolutionsFrameworkService",
    "HPOmenCap",
    "HPAppHelperCap",
    "HPNetworkCap"
)

$found = 0
foreach ($svc in $hpServices) {
    $status = Get-Service -Name $svc -ErrorAction SilentlyContinue
    if ($status -and $status.Status -eq 'Running') {
        Write-Host "     [!] Detected active HP bloat service: $svc" -ForegroundColor Yellow
        $found++
    }
}

if ($found -eq 0) {
    Write-Host "     [+] HP ecosystem is clean. No active telemetry services found." -ForegroundColor Green
} else {
    Write-Host "         WHY: HP background services frequently launch telemetry scans and network polling, interrupting deep system idle." -ForegroundColor Gray
}
