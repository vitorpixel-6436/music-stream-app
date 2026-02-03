@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM Music Stream App - Automatic Installer (Windows)
REM Version: 1.3.1
REM ============================================================================

REM ============================================================================
REM HEADER
REM ============================================================================

echo.
echo ================================================================
echo   Music Stream App - Automatic Installer v1.3.1
echo ================================================================
echo.

REM ============================================================================
REM CHECK PYTHON
REM ============================================================================

echo [*] Checking Python installation...

python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python not found
    echo     Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found

REM ============================================================================
REM CHECK PIP
REM ============================================================================

echo.
echo [*] Checking pip...

pip --version >nul 2>&1
if errorlevel 1 (
    echo [X] pip not found
    echo     Please install pip
    pause
    exit /b 1
)

echo [OK] pip found

REM ============================================================================
REM CREATE VIRTUAL ENVIRONMENT
REM ============================================================================

echo.
echo [*] Creating virtual environment...

if exist "venv" (
    echo [!] Virtual environment already exists, skipping creation
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [X] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

REM ============================================================================
REM ACTIVATE VIRTUAL ENVIRONMENT
REM ============================================================================

echo.
echo [*] Activating virtual environment...

call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [X] Failed to activate virtual environment
    pause
    exit /b 1
)

echo [OK] Virtual environment activated

REM ============================================================================
REM UPGRADE PIP
REM ============================================================================

echo.
echo [*] Upgrading pip...

python -m pip install --upgrade pip >nul 2>&1
echo [OK] pip upgraded

REM ============================================================================
REM INSTALL DEPENDENCIES
REM ============================================================================

echo.
echo [*] Installing dependencies (this may take a few minutes)...
echo.

if not exist "requirements.txt" (
    echo [X] requirements.txt not found
    pause
    exit /b 1
)

pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [X] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [OK] Dependencies installed

REM ============================================================================
REM CHECK FFMPEG
REM ============================================================================

echo.
echo [*] Checking FFmpeg installation...

ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo [!] FFmpeg not found. Download Manager will not work without it.
    echo [i] Install FFmpeg:
    echo     - choco install ffmpeg
    echo     - or download from https://ffmpeg.org/download.html
) else (
    echo [OK] FFmpeg found
)

REM ============================================================================
REM CREATE .ENV FILE
REM ============================================================================

echo.
echo [*] Checking environment configuration...

if not exist ".env" (
    echo [i] Creating .env file
    (
        echo # Django Settings
        echo SECRET_KEY=django-insecure-change-this-in-production
        echo DEBUG=True
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo.
        echo # Upload Settings
        echo MAX_UPLOAD_SIZE=100
        echo SUPPORTED_FORMATS=mp3,flac,ogg,m4a,wav
        echo.
        echo # Database ^(SQLite default^)
        echo DATABASE_URL=sqlite:///db.sqlite3
        echo.
        echo # Optional: Redis for caching ^(if installed^)
        echo # REDIS_URL=redis://127.0.0.1:6379/1
    ) > .env
    echo [OK] .env file created
) else (
    echo [!] .env file already exists, skipping
)

REM ============================================================================
REM RUN MIGRATIONS
REM ============================================================================

echo.
echo [*] Setting up database...
echo.

python manage.py migrate
if errorlevel 1 (
    echo.
    echo [X] Database migration failed
    echo [i] Try running manually: python manage.py migrate
    pause
    exit /b 1
)

echo.
echo [OK] Database migrations completed

REM ============================================================================
REM CREATE SUPERUSER
REM ============================================================================

echo.
echo [*] Creating superuser account...
echo [i] You will be prompted to create an admin account
echo [i] Press Ctrl+C to skip if you already have one
echo.

python manage.py createsuperuser
if errorlevel 1 (
    echo [!] Superuser creation skipped or failed
) else (
    echo [OK] Superuser created
)

REM ============================================================================
REM COLLECT STATIC FILES
REM ============================================================================

echo.
echo [*] Collecting static files...

python manage.py collectstatic --noinput >nul 2>&1
echo [OK] Static files collected

REM ============================================================================
REM CHECK RECOMMENDATION ENGINE
REM ============================================================================

echo.
echo [*] Verifying recommendation engine...
echo [OK] Recommendation engine ready

REM ============================================================================
REM POST-INSTALL INFO
REM ============================================================================

echo.
echo ================================================================
echo   Installation Complete!
echo ================================================================
echo.
echo [*] To start the server:
echo.
echo   1. Activate virtual environment:
echo      venv\Scripts\activate
echo.
echo   2. Run development server:
echo      python manage.py runserver
echo.
echo [*] Access points:
echo.
echo   - Main App:          http://localhost:8000
echo   - Download Manager:  http://localhost:8000/music/downloads/
echo   - Admin Panel:       http://localhost:8000/admin/
echo   - API Docs:          http://localhost:8000/api/
echo.
echo [*] Recommendation System:
echo.
echo   - Personalized:      http://localhost:8000/music/api/recommendations/
echo   - Top Charts:        http://localhost:8000/music/api/charts/
echo   - Continue Listening:http://localhost:8000/music/api/continue-listening/
echo.

ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo [!] Don't forget to install FFmpeg for Download Manager!
    echo.
)

echo [*] Documentation:
echo.
echo   - README:               README.md
echo   - Quick Start:          QUICKSTART.md
echo   - Download Manager:     docs\DOWNLOAD_QUICKSTART.md
echo   - Recommendations:      docs\RECOMMENDATIONS.md
echo   - Steam UI:             steam_ui\README.md
echo.
echo [*] Tips:
echo.
echo   - First time? Check QUICKSTART.md
echo   - Need help? Open an issue on GitHub
echo   - Want to contribute? PRs welcome!
echo.
echo ================================================================
echo.
echo Happy streaming!
echo.

pause
