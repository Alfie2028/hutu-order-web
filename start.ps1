# One-click launcher (cloudflared): backend + H5 page + two public tunnels.
# No signup, no IP-verification page. Paths derived at runtime.
$ErrorActionPreference = "Continue"

$root      = $PSScriptRoot
$serverDir = Join-Path $root "hutu-order-server"
$webDir    = Join-Path $root "hutu-order-web"
$h5Dir     = Join-Path $webDir "dist\build\h5"
$reqFile   = Join-Path $webDir "src\utils\request.js"
$cf        = Join-Path $root "cloudflared.exe"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Campus Ordering - One-Click (cloudflared)"
Write-Host "======================================" -ForegroundColor Cyan

function Test-Port($port) {
    try {
        $r = Invoke-WebRequest -Uri "http://127.0.0.1:$port" -UseBasicParsing -TimeoutSec 2
        return $true
    } catch { return $false }
}

if (-not (Test-Path $cf)) {
    Write-Host "  cloudflared.exe NOT FOUND next to this script. Abort." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# [1/5] Backend 8000
Write-Host "`n[1/5] Backend..." -ForegroundColor Yellow
if (Test-Port 8000) {
    Write-Host "  Backend already running." -ForegroundColor Green
} else {
    Write-Host "  Starting backend in a new window..." -ForegroundColor Yellow
    Start-Process powershell -WorkingDirectory $serverDir -ArgumentList '-NoExit','-Command','python -m uvicorn main:app --host 0.0.0.0 --port 8000'
    $ok = $false
    for ($i = 0; $i -lt 20; $i++) { Start-Sleep -Seconds 1; if (Test-Port 8000) { $ok = $true; break } }
    if ($ok) { Write-Host "  Backend up." -ForegroundColor Green } else { Write-Host "  Backend start timed out. Check the new window." -ForegroundColor Red }
}

# [2/5] H5 static server 8080
Write-Host "`n[2/5] H5 static server..." -ForegroundColor Yellow
if (Test-Port 8080) {
    Write-Host "  Static server already running." -ForegroundColor Green
} else {
    Write-Host "  Starting static server (background)..." -ForegroundColor Yellow
    Start-Process python -ArgumentList '-m','http.server','8080' -WorkingDirectory $h5Dir -WindowStyle Hidden
    $ok = $false
    for ($i = 0; $i -lt 15; $i++) { Start-Sleep -Seconds 1; if (Test-Port 8080) { $ok = $true; break } }
    if ($ok) { Write-Host "  Static server up." -ForegroundColor Green } else { Write-Host "  Static server start failed." -ForegroundColor Red }
}

# 清理残留 cloudflared 进程（旧进程会占用日志文件，导致删除失败）
Get-Process cloudflared -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Milliseconds 500

# [3/5] Backend tunnel -> 8000
Write-Host "`n[3/5] Backend tunnel..." -ForegroundColor Yellow
$backendUrl = $null
$log1 = Join-Path $env:TEMP "cf-backend.log"
if (Test-Path $log1) { try { Remove-Item $log1 -Force -ErrorAction Stop } catch {} }
if (Test-Path "$log1.err") { try { Remove-Item "$log1.err" -Force -ErrorAction Stop } catch {} }
Start-Process $cf -ArgumentList 'tunnel','--url','http://localhost:8000','--protocol','http2' -RedirectStandardOutput $log1 -RedirectStandardError "$log1.err" -WindowStyle Hidden
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Seconds 1
    $c = ""
    if (Test-Path $log1) { $c += Get-Content $log1 -Raw -ErrorAction SilentlyContinue }
    if (Test-Path "$log1.err") { $c += Get-Content "$log1.err" -Raw -ErrorAction SilentlyContinue }
    if ($c -match "https://[a-z0-9-]+\.trycloudflare\.com") { $backendUrl = $Matches[0]; break }
}
if ($backendUrl) { Write-Host "  Backend URL: $backendUrl" -ForegroundColor Green } else { Write-Host "  Failed to get backend URL." -ForegroundColor Red }

# [4/5] H5 tunnel -> 8080
Write-Host "`n[4/5] H5 page tunnel..." -ForegroundColor Yellow
$h5Url = $null
$log2 = Join-Path $env:TEMP "cf-h5.log"
if (Test-Path $log2) { try { Remove-Item $log2 -Force -ErrorAction Stop } catch {} }
if (Test-Path "$log2.err") { try { Remove-Item "$log2.err" -Force -ErrorAction Stop } catch {} }
Start-Process $cf -ArgumentList 'tunnel','--url','http://localhost:8080','--protocol','http2' -RedirectStandardOutput $log2 -RedirectStandardError "$log2.err" -WindowStyle Hidden
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Seconds 1
    $c = ""
    if (Test-Path $log2) { $c += Get-Content $log2 -Raw -ErrorAction SilentlyContinue }
    if (Test-Path "$log2.err") { $c += Get-Content "$log2.err" -Raw -ErrorAction SilentlyContinue }
    if ($c -match "https://[a-z0-9-]+\.trycloudflare\.com") { $h5Url = $Matches[0]; break }
}
if ($h5Url) { Write-Host "  H5 URL: $h5Url" -ForegroundColor Green } else { Write-Host "  Failed to get H5 URL." -ForegroundColor Red }

# [5/5] Update frontend BASE_URL + rebuild H5
if ($backendUrl) {
    Write-Host "`n[5/5] Update BASE_URL + rebuild H5..." -ForegroundColor Yellow
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    $content = [System.IO.File]::ReadAllText($reqFile, [System.Text.Encoding]::UTF8)
    $content = $content -replace "const BASE_URL = '[^']*'", "const BASE_URL = '$backendUrl'"
    [System.IO.File]::WriteAllText($reqFile, $content, $utf8NoBom)
    Push-Location $webDir
    npm run build:h5
    Pop-Location
}

Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "  DONE!"
Write-Host "  H5 page  : $h5Url" -ForegroundColor Green
Write-Host "  Backend  : $backendUrl" -ForegroundColor Green
Write-Host "  Open the H5 page in any browser. No signup, no IP page."
Write-Host "  Use stop.bat to stop the tunnels."
Write-Host "======================================" -ForegroundColor Cyan
Read-Host "Press Enter to exit (tunnels keep running in background)"
