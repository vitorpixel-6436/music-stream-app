#!/bin/bash

# Music Streaming App - Automated Installation Script
# Поддержка: Ubuntu 20.04+, Debian 10+, CentOS 7+

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Функции
print_status() {
    echo -e "${GREEN}[*]${NC} $1"
}

print_error() {
    echo -e "${RED}[!]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[?]${NC} $1"
}

# Проверка прав администратора
if [[ $EUID -ne 0 ]]; then
    print_error "Этот скрипт должен быть запущен от sudo"
    exit 1
fi

print_status "Начало установки Music Streaming App..."

# Определение ОС
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    print_error "Не удаётся определить ОС"
    exit 1
fi

print_status "Обнаружена ОС: $OS"

# Обновление системных пакетов
print_status "Обновление системных пакетов..."
case $OS in
    ubuntu|debian)
        apt-get update -qq
        apt-get upgrade -y -qq
        ;;
    centos|rhel)
        yum update -y -q
        ;;
    *)
        print_warning "ОС не поддерживается полностью"
        ;;
esac

# Установка зависимостей
print_status "Установка системных зависимостей..."
case $OS in
    ubuntu|debian)
        apt-get install -y -qq \
            python3.11 \
            python3.11-venv \
            python3-pip \
            postgresql \
            postgresql-contrib \
            redis-server \
            git \
            curl \
            wget \
            ffmpeg \
            build-essential \
            libpq-dev \
            docker.io \
            docker-compose
        ;;
    centos|rhel)
        yum install -y -q \
            python311 \
            python311-devel \
            postgresql-server \
            postgresql-contrib \
            redis \
            git \
            curl \
            wget \
            ffmpeg \
            gcc \
            make \
            docker \
            docker-compose
        ;;
esac

# Запуск сервисов БД
print_status "Запуск PostgreSQL и Redis..."
systemctl start postgresql || true
systemctl start redis-server || true
systemctl enable postgresql || true
systemctl enable redis-server || true

# Клонирование репозитория
if [ ! -d "music-stream-app" ]; then
    print_status "Клонирование репозитория..."
    git clone https://github.com/vitorpixel-6436/music-stream-app.git
else
    print_status "Репозиторий уже существует, обновление..."
    cd music-stream-app
    git pull origin main
    cd ..
fi

cd music-stream-app

# Создание виртуального окружения
print_status "Создание виртуального окружения Python..."
python3.11 -m venv venv || python3 -m venv venv
source venv/bin/activate

# Обновление pip
print_status "Обновление pip..."
pip install --upgrade pip setuptools wheel

# Установка Python зависимостей
print_status "Установка Python зависимостей..."
pip install -r requirements.txt

# Создание файла .env
if [ ! -f ".env" ]; then
    print_status "Создание файла .env..."
    cp .env.example .env || cat > .env << 'EOF'
DEBUG=False
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=localhost,127.0.0.1,*
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/music_stream
REDIS_URL=redis://localhost:6379/0
EOF
fi

# Создание базы данных
print_status "Создание базы данных PostgreSQL..."
sudo -u postgres createdb music_stream || true

# Миграции БД
print_status "Выполнение миграций БД..."
python manage.py migrate

# Создание суперпользователя
print_status "Создание суперпользователя..."
python manage.py createsuperuser --noinput --username admin --email admin@localhost.com || true

# Сбор статических файлов
print_status "Сбор статических файлов..."
python manage.py collectstatic --noinput

# Создание директорий для медиа
print_status "Создание директорий для медиа файлов..."
mkdir -p media logs
chown -R $SUDO_USER:$SUDO_USER . || true

print_status ""
print_status "═══════════════════════════════════════════════════════════"
print_status "✓ Установка успешно завершена!"
print_status "═══════════════════════════════════════════════════════════"
print_status ""
print_status "Для запуска в режиме разработки:"
echo -e "  ${YELLOW}source venv/bin/activate${NC}"
echo -e "  ${YELLOW}python manage.py runserver 0.0.0.0:8000${NC}"
echo -e ""
print_status "Для запуска с Docker:"
echo -e "  ${YELLOW}docker-compose up -d${NC}"
echo -e ""
print_status "Веб-интерфейс: http://localhost:8000"
print_status "Админ-панель: http://localhost:8000/admin"
print_status ""
print_status "Документация: см. DEPLOYMENT_GUIDE.md"
print_status ""
