@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"

REM ========================================
REM  AUTO-DETECT NETWORK CONFIGURATION
REM ========================================

REM Get local IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4" ^| findstr /v "127.0.0.1"') do (
    set "LOCAL_IP=%%a"
    goto :ip_found
)
:ip_found
set "LOCAL_IP=%LOCAL_IP:~1%"

REM Get Wi-Fi network name
for /f "tokens=2 delims=:" %%a in ('netsh wlan show interfaces ^| findstr "SSID" ^| findstr /v "BSSID"') do (
    set "WIFI=%%a"
    goto :wifi_found
)
:wifi_found
set "WIFI=%WIFI:~1%"

REM Update .env with current IP
if exist ".env" (
    powershell -Command "(Get-Content .env) -replace 'ALLOWED_HOSTS=.*', 'ALLOWED_HOSTS=localhost,127.0.0.1,%LOCAL_IP%,*' | Set-Content .env"
)

REM Activate virtual environment
call venv\Scripts\activate.bat

cls
color 0A

echo.
echo ========================================
echo  🎵 Music Streaming App - Network Mode
echo ========================================
echo.
echo ✅ Server Starting...
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo  📍 LOCAL ACCESS:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo    → http://localhost:8000
echo    → http://127.0.0.1:8000
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo  📱 MOBILE/NETWORK ACCESS:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if defined WIFI (
    echo    Wi-Fi Network: %WIFI%
) else (
    echo    ⚠️  Wi-Fi info not detected
)
if defined LOCAL_IP (
    echo    Your IP: %LOCAL_IP%
    echo    → http://%LOCAL_IP%:8000
) else (
    echo    ⚠️  IP address not detected
    echo    Run: ipconfig
    echo    Look for "IPv4 Address"
)
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo  💡 HOW TO CONNECT FROM PHONE:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if defined WIFI (
    echo    1. Connect phone to Wi-Fi: "%WIFI%"
) else (
    echo    1. Connect phone to SAME Wi-Fi as PC
)
if defined LOCAL_IP (
    echo    2. Open browser on phone
    echo    3. Enter: http://%LOCAL_IP%:8000
) else (
    echo    2. Check PC IP: ipconfig
    echo    3. Open http://[YOUR-IP]:8000 on phone
)
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo  ⚠️  TROUBLESHOOTING:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo    Can't connect? Try:
echo.
echo    ✓ Check both devices on SAME Wi-Fi
echo    ✓ Disable VPN on PC
echo    ✓ Allow port 8000 in Windows Firewall:
echo.
echo      Run as Administrator:
echo      netsh advfirewall firewall add rule ^
echo      name="Music App" dir=in action=allow ^
echo      protocol=TCP localport=8000
echo.
echo    ✓ Restart router if still not working
echo    ✓ Try disabling Windows Firewall temporarily
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo  ℹ️  ADMIN PANEL:
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if defined LOCAL_IP (
    echo    Local:   http://localhost:8000/admin
    echo    Network: http://%LOCAL_IP%:8000/admin
) else (
    echo    → http://localhost:8000/admin
)
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo  Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

REM Start Django server on all interfaces
python manage.py runserver 0.0.0.0:8000

echo.
echo Server stopped.
pause
