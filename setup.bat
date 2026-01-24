@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"

echo ========================================
echo   Music Streaming App - Setup
echo ========================================
echo.

REM Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python 3.10 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo [OK] Python %PYVER% found
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment!
        echo.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] activate.bat not found in venv\Scripts\
    echo.
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment
    echo.
    pause
    exit /b 1
)
echo [OK] Environment activated
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
echo This may take several minutes...
echo.
python -m pip install --upgrade pip --quiet
if %errorlevel% neq 0 (
    echo [WARNING] Failed to upgrade pip, continuing anyway...
)

pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies!
    echo.
    echo Try running manually:
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)
echo.
echo [OK] Dependencies installed successfully
echo.

REM Create .env file
if not exist ".env" (
    echo Creating .env configuration file...
    (
        echo SECRET_KEY=django-insecure-local-dev-key-change-this-in-production
        echo DEBUG=True
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo DATABASE_URL=sqlite:///db.sqlite3
    ) > .env
    echo [OK] .env file created
    echo.
)

REM Database setup
echo [5/5] Setting up database...
python manage.py makemigrations --noinput >nul 2>&1
python manage.py migrate --noinput
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Database migration failed!
    echo.
    echo Please check:
    echo   - manage.py exists in current directory
    echo   - Django is installed correctly
    echo.
    pause
    exit /b 1
)
echo [OK] Database configured successfully
echo.

REM Create start.bat
echo Creating start.bat launcher...
(
    echo @echo off
    echo chcp 65001 ^>nul 2^>^&1
    echo cd /d "%%~dp0"
    echo call venv\Scripts\activate.bat
    echo cls
    echo echo ========================================
    echo echo   Music Streaming App
    echo echo ========================================
    echo echo.
    echo echo Server starting...
    echo echo.
    echo echo Open your browser and go to:
    echo echo   http://localhost:8000
    echo echo.
    echo echo Admin panel:
    echo echo   http://localhost:8000/admin
    echo echo.
    echo echo Press Ctrl+C to stop the server
    echo echo.
    echo python manage.py runserver
    echo pause
) > start.bat
echo [OK] start.bat created
echo.

REM Offer to create superuser
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Would you like to create an admin user now? (Y/N)
set /p create_admin=Your choice: 
if /i "%create_admin%"=="Y" (
    echo.
    echo Creating admin user...
    echo.
    python manage.py createsuperuser
)

REM Final instructions
echo.
echo ========================================
echo   Ready to use!
echo ========================================
echo.
echo To start the application, run:
echo   start.bat
echo.
echo Then open your browser and go to:
echo   http://localhost:8000
echo.
echo Admin panel is available at:
echo   http://localhost:8000/admin
echo.
echo.
echo Press any key to exit setup...
pause >nul
