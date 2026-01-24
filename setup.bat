@echo off
chcp 65001 >nul
echo ========================================
echo  Music Streaming App - Установка
echo ========================================
echo.

REM Проверка наличия Python
echo [1/5] Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python не установлен!
    echo.
    echo Скачайте Python 3.10+ с https://www.python.org/downloads/
    echo Не забудьте отметить "Add Python to PATH" при установке!
    pause
    exit /b 1
)
echo [OK] Python найден

REM Создание виртуального окружения
echo.
echo [2/5] Создание виртуального окружения...
if not exist "venv" (
    python -m venv venv
    echo [OK] Виртуальное окружение создано
) else (
    echo [OK] Виртуальное окружение уже существует
)

REM Активация виртуального окружения
echo.
echo [3/5] Активация окружения...
call venv\Scripts\activate.bat
echo [OK] Окружение активировано

REM Установка зависимостей
echo.
echo [4/5] Установка зависимостей...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Ошибка установки зависимостей!
    pause
    exit /b 1
)
echo [OK] Зависимости установлены

REM Создание .env файла
echo.
if not exist ".env" (
    echo SECRET_KEY=django-insecure-local-dev-key-change-in-production > .env
    echo DEBUG=True >> .env
    echo ALLOWED_HOSTS=localhost,127.0.0.1 >> .env
    echo [OK] Файл .env создан
)

REM Применение миграций
echo.
echo [5/5] Настройка базы данных...
python manage.py makemigrations music >nul 2>&1
python manage.py migrate
if errorlevel 1 (
    echo [ERROR] Ошибка миграции базы данных!
    pause
    exit /b 1
)
echo [OK] База данных настроена

REM Создание суперпользователя (опционально)
echo.
echo ========================================
echo  Установка завершена!
echo ========================================
echo.
echo Хотите создать администратора? (Y/N)
set /p create_admin=
if /i "%create_admin%"=="Y" (
    echo.
    echo Создание администратора...
    python manage.py createsuperuser
)

REM Создание ярлыка для запуска
echo.
echo Создание ярлыка для запуска...

echo @echo off > start.bat
echo chcp 65001 ^>nul >> start.bat
echo call venv\Scripts\activate.bat >> start.bat
echo echo ======================================== >> start.bat
echo echo  Music Streaming App запущен! >> start.bat
echo echo ======================================== >> start.bat
echo echo. >> start.bat
echo echo Откройте браузер и перейдите: >> start.bat
echo echo http://localhost:8000 >> start.bat
echo echo. >> start.bat
echo echo Админ-панель: http://localhost:8000/admin >> start.bat
echo echo. >> start.bat
echo echo Нажмите Ctrl+C для остановки сервера >> start.bat
echo echo. >> start.bat
echo python manage.py runserver >> start.bat
echo pause >> start.bat

echo [OK] Ярлык start.bat создан

echo.
echo ========================================
echo  Готово!
echo ========================================
echo.
echo Для запуска приложения:
echo 1. Запустите start.bat
echo 2. Откройте браузер: http://localhost:8000
echo.
echo Админ-панель: http://localhost:8000/admin
echo.
pause
