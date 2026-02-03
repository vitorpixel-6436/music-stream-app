@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM Music Stream App - Automatic Installer (Windows)
REM Version: 1.3.0
REM ============================================================================

REM Enable UTF-8 encoding
chcp 65001 >nul 2>&1

REM Colors (Windows 10+ only)
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

REM ============================================================================
REM HEADER
REM ============================================================================

echo.
echo %BLUE%================================================================%NC%
echo %BLUE%  Music Stream App - Automatic Installer v1.3.0%NC%
echo %BLUE%================================================================%NC%
echo.

REM ============================================================================
REM CHECK PYTHON
REM ============================================================================

echo %BLUE%[*]%NC% Checking Python installation...

python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%[X] Python not found%NC%
    echo %RED%Please install Python 3.10+ from https://www.python.org/%NC%
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo %GREEN%[OK] Python %PYTHON_VERSION% found%NC%

REM ============================================================================
REM CHECK PIP
REM ============================================================================

echo.
echo %BLUE%[*]%NC% Checking pip...

pip --version >nul 2>&1
if errorlevel 1 (
    echo %RED%[X] pip not found%NC%
    echo %RED%Please install pip%NC%
    pause
    exit /b 1
)

echo %GREEN%[OK] pip found%NC%

REM ============================================================================
REM CREATE VIRTUAL ENVIRONMENT
REM ============================================================================

echo.
echo %BLUE%[*]%NC% Creating virtual environment...

if exist "venv" (
    echo %YELLOW%[!] Virtual environment already exists, skipping creation%NC%
) else (
    python -m venv venv
    if errorlevel 1 (
        echo %RED%[X] Failed to create virtual environment%NC%
        pause
        exit /b 1
    )
    echo %GREEN%[OK] Virtual environment created%NC%
)

REM ============================================================================
REM ACTIVATE VIRTUAL ENVIRONMENT
REM ============================================================================

echo.
echo %BLUE%[*]%NC% Activating virtual environment...

call venv\Scripts\activate.bat
if errorlevel 1 (
    echo %RED%[X] Failed to activate virtual environment%NC%
    pause
    exit /b 1
)

echo %GREEN%[OK] Virtual environment activated%NC%

REM ============================================================================
REM UPGRADE PIP
REM ============================================================================

echo.
echo %BLUE%[*]%NC% Upgrading pip...

python -m pip install --upgrade pip >nul 2>&1
echo %GREEN%[OK] pip upgraded%NC%

REM ============================================================================
REM INSTALL DEPENDENCIES
REM ============================================================================

echo.
echo %BLUE%[*]%NC% Installing dependencies (this may take a few minutes)...

if not exist "requirements.txt" (
    echo %RED%[X] requirements.txt not found%NC%
    pause
    exit /b 1
)

pip install -r requirements.txt
if errorlevel 1 (
    echo %RED%[X] Failed to install dependencies%NC%
    pause
    exit /b 1
)

echo %GREEN%[OK] Dependencies installed%NC%

REM ============================================================================
REM CHECK FFMPEG
REM ============================================================================

echo.
echo %BLUE%[*]%NC% Checking FFmpeg installation...

ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo %YELLOW%[!] FFmpeg not found. Download Manager will not work without it.%NC%
    echo %YELLOW%[i] Install FFmpeg:%NC%
    echo     choco install ffmpeg
    echo     or download from https://ffmpeg.org/download.html
) else (
    echo %GREEN%[OK] FFmpeg found%NC%
)

REM ============================================================================
REM CREATE .ENV FILE
REM ============================================================================

echo.
echo %BLUE%[*]%NC% Checking environment configuration...

if not exist ".env" (
    echo %BLUE%[i] Creating .env file%NC%
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
    echo %GREEN%[OK] .env file created%NC%
) else (
    echo %YELLOW%[!] .env file already exists, skipping%NC%
)

REM ============================================================================
REM RUN MIGRATIONS
REM ============================================================================

echo.
echo %BLUE%[*]%NC% Setting up database...

python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo %RED%[X] Database migration failed%NC%
    pause
    exit /b 1
)

echo %GREEN%[OK] Database migrations completed%NC%

REM ============================================================================
REM CREATE SUPERUSER
REM ============================================================================

echo.
echo %BLUE%[*]%NC% Creating superuser account...
echo %BLUE%[i] You will be prompted to create an admin account%NC%
echo %BLUE%[i] Press Ctrl+C to skip if you already have one%NC%
echo.

python manage.py createsuperuser
if errorlevel 1 (
    echo %YELLOW%[!] Superuser creation skipped or failed%NC%
) else (
    echo %GREEN%[OK] Superuser created%NC%
)

REM ============================================================================
REM COLLECT STATIC FILES
REM ============================================================================

echo.
echo %BLUE%[*]%NC% Collecting static files...

python manage.py collectstatic --noinput >nul 2>&1
echo %GREEN%[OK] Static files collected%NC%

REM ============================================================================
REM CHECK RECOMMENDATION ENGINE
REM ============================================================================

echo.
echo %BLUE%[*]%NC% Checking recommendation engine setup...

python manage.py showmigrations music | findstr "ListeningHistory" >nul 2>&1
if errorlevel 1 (
    echo %BLUE%[i] Recommendation engine migrations detected, applying...%NC%
    python manage.py migrate music
    echo %GREEN%[OK] Recommendation engine ready%NC%
) else (
    echo %GREEN%[OK] Recommendation engine database ready%NC%
)

REM ============================================================================
REM POST-INSTALL INFO
REM ============================================================================

echo.
echo %GREEN%================================================================%NC%
echo %GREEN%  Installation Complete!%NC%
echo %GREEN%================================================================%NC%
echo.
echo %BLUE%[*] To start the server:%NC%
echo.
echo   1. Activate virtual environment:
echo      %GREEN%venv\Scripts\activate%NC%
echo.
echo   2. Run development server:
echo      %GREEN%python manage.py runserver%NC%
echo.
echo %BLUE%[*] Access points:%NC%
echo.
echo   - Main App:          %GREEN%http://localhost:8000%NC%
echo   - Download Manager:  %GREEN%http://localhost:8000/music/downloads/%NC%
echo   - Admin Panel:       %GREEN%http://localhost:8000/admin/%NC%
echo   - API Docs:          %GREEN%http://localhost:8000/api/%NC%
echo.
echo %BLUE%[*] Recommendation System:%NC%
echo.
echo   - Personalized:      %GREEN%http://localhost:8000/music/api/recommendations/%NC%
echo   - Top Charts:        %GREEN%http://localhost:8000/music/api/charts/%NC%
echo   - Continue Listening:%GREEN%http://localhost:8000/music/api/continue-listening/%NC%
echo.

ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo %YELLOW%[!] Don't forget to install FFmpeg for Download Manager!%NC%
    echo.
)

echo %BLUE%[*] Documentation:%NC%
echo.
echo   - README:               %GREEN%README.md%NC%
echo   - Download Manager:     %GREEN%docs\DOWNLOAD_QUICKSTART.md%NC%
echo   - Recommendations:      %GREEN%docs\RECOMMENDATIONS.md%NC%
echo   - Steam UI:             %GREEN%steam_ui\README.md%NC%
echo.
echo %BLUE%[*] Tips:%NC%
echo.
echo   - First time? Check %GREEN%docs\DOWNLOAD_QUICKSTART.md%NC%
echo   - Need help? Open an issue on GitHub
echo   - Want to contribute? PRs welcome!
echo.
echo %GREEN%================================================================%NC%
echo.
echo %GREEN%Happy streaming!%NC%
echo.

pause
