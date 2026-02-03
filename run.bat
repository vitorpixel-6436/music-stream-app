@echo off
REM ============================================================================
REM Music Stream App - Quick Start Script
REM Version: 1.0
REM ============================================================================

echo.
echo ================================================================
echo   Music Stream App - Starting Server
echo ================================================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo [X] Virtual environment not found!
    echo [i] Please run install.bat first
    pause
    exit /b 1
)

echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

echo [*] Starting Django development server...
echo.
echo [OK] Server starting at http://localhost:8000
echo [i] Press Ctrl+C to stop the server
echo.

REM Start the server
python manage.py runserver

REM If server stops, pause to see any errors
echo.
echo [!] Server stopped
pause
