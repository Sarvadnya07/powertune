param(
    [string]$Profile = "unknown"
)

$snapshotsDir = Join-Path $PSScriptRoot "snapshots"
if (!(Test-Path $snapshotsDir)) { New-Item -ItemType Directory -Path $snapshotsDir | Out-Null }

$dateStr = Get-Date -Format "yyyy-MM-dd_HHmmss"
$snapshotFile = Join-Path $snapshotsDir "snapshot_$dateStr.json"

Write-Host "     [*] Creating rollback snapshot..." -ForegroundColor Yellow
$activeScheme = powercfg /getactivescheme | Select-String -Pattern "GUID: ([a-f0-9\-]+)" | % { $_.Matches.Groups[1].Value }

$minAcRaw = powercfg /q SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN | Select-String "Current AC Power Setting Index" | ForEach-Object { $_.ToString().Split(":")[1].Trim() }
$minDcRaw = powercfg /q SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN | Select-String "Current DC Power Setting Index" | ForEach-Object { $_.ToString().Split(":")[1].Trim() }
$maxAcRaw = powercfg /q SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX | Select-String "Current AC Power Setting Index" | ForEach-Object { $_.ToString().Split(":")[1].Trim() }
$maxDcRaw = powercfg /q SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX | Select-String "Current DC Power Setting Index" | ForEach-Object { $_.ToString().Split(":")[1].Trim() }

$snapshotData = @{
    Timestamp = (Get-Date -Format s)
    Profile = $Profile
    ActiveScheme = $activeScheme
    CpuMinAc = if ($minAcRaw) { [Convert]::ToInt32($minAcRaw, 16) } else { $null }
    CpuMinDc = if ($minDcRaw) { [Convert]::ToInt32($minDcRaw, 16) } else { $null }
    CpuMaxAc = if ($maxAcRaw) { [Convert]::ToInt32($maxAcRaw, 16) } else { $null }
    CpuMaxDc = if ($maxDcRaw) { [Convert]::ToInt32($maxDcRaw, 16) } else { $null }
    Services = (Get-Service | Select-Object Name, Status, StartType | ForEach-Object { 
        @{ Name = $_.Name; Status = $_.Status.ToString(); StartType = $_.StartType.ToString() }
    })
}

$snapshotData | ConvertTo-Json | Out-File -FilePath $snapshotFile -Encoding UTF8

Write-Host "     [+] Snapshot saved to $snapshotFile" -ForegroundColor Green
