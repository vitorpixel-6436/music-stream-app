@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

echo ========================================
echo  Music Streaming App - Setup
echo ========================================
echo.

REM Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo.
    echo Download Python 3.10+ from https://www.python.org/downloads/
    echo Don't forget to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo [OK] Python !PYVER! found

REM Create virtual environment
echo.
echo [2/5] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Activate virtual environment
echo.
echo [3/5] Activating environment...
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] venv\Scripts\activate.bat not found!
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)
echo [OK] Environment activated

REM Install dependencies
echo.
echo [4/5] Installing dependencies...
echo This may take a few minutes...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [ERROR] Failed to upgrade pip!
    pause
    exit /b 1
)

pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    echo.
    echo Try running: pip install -r requirements.txt
    pause
    exit /b 1
)
echo [OK] Dependencies installed

REM Create .env file
echo.
if not exist ".env" (
    (
        echo SECRET_KEY=django-insecure-local-dev-key-!random!!random!
        echo DEBUG=True
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo DATABASE_URL=sqlite:///db.sqlite3
    ) > .env
    echo [OK] .env file created
)

REM Database migrations
echo.
echo [5/5] Setting up database...
python manage.py makemigrations --noinput >nul 2>&1
python manage.py migrate --noinput
if errorlevel 1 (
    echo [ERROR] Database migration failed!
    echo.
    echo Check if manage.py exists and Django is installed correctly
    pause
    exit /b 1
)
echo [OK] Database configured

REM Create superuser prompt
echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Create admin user? (Y/N)
set /p create_admin=
if /i "!create_admin!"=="Y" (
    echo.
    echo Creating administrator...
    python manage.py createsuperuser
)

REM Create start.bat
echo.
echo Creating start.bat launcher...
(
    echo @echo off
    echo chcp 65001 ^>nul 2^>^&1
    echo cd /d "%%~dp0"
    echo call venv\Scripts\activate.bat
    echo echo ========================================
    echo echo  Music Streaming App Started!
    echo echo ========================================
    echo echo.
    echo echo Open browser: http://localhost:8000
    echo echo Admin panel: http://localhost:8000/admin
    echo echo.
    echo echo Press Ctrl+C to stop server
    echo echo.
    echo python manage.py runserver
    echo pause
) > start.bat
echo [OK] start.bat created

echo.
echo ========================================
echo  Ready!
echo ========================================
echo.
echo To start the application:
echo 1. Run start.bat
echo 2. Open browser: http://localhost:8000
echo.
echo Admin panel: http://localhost:8000/admin
echo.
echo.
pause
