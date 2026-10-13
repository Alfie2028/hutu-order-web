@echo off
taskkill /f /im cloudflared.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1
echo.
echo Tunnels stopped (cloudflared + node).
echo Close the backend window to stop the backend too.
echo.
pause
