param(
    [switch]$DiagnosticOnly
)

Write-Host "     [*] Dell Vendor Module: Scanning for SupportAssist & Optimizer Bloat" -ForegroundColor Gray

$dellServices = @(
    "DellSupportAssist",
    "DellHardwareSupport",
    "DellOptimizer",
    "DellClientManagementService"
)

$found = 0
foreach ($svc in $dellServices) {
    $status = Get-Service -Name $svc -ErrorAction SilentlyContinue
    if ($status -and $status.Status -eq 'Running') {
        Write-Host "     [!] Detected active Dell bloat service: $svc" -ForegroundColor Yellow
        $found++
    }
}

if ($found -eq 0) {
    Write-Host "     [+] Dell ecosystem is clean. No active bloat services found." -ForegroundColor Green
} else {
    Write-Host "         WHY: Dell SupportAssist frequently runs automated hardware scans in the background, spiking CPU usage to 100% and draining battery." -ForegroundColor Gray
}
