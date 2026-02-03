#!/bin/bash

##############################################################################
# Music Stream App - Automatic Installer (Linux/macOS)
# Version: 1.3.0
##############################################################################

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Emojis
CHECK="${GREEN}✓${NC}"
CROSS="${RED}✗${NC}"
INFO="${BLUE}ℹ${NC}"
WARN="${YELLOW}⚠${NC}"

##############################################################################
# FUNCTIONS
##############################################################################

print_header() {
    echo -e ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  🎵 Music Stream App - Automatic Installer v1.3.0${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e ""
}

print_step() {
    echo -e "\n${BLUE}▶${NC} $1..."
}

print_success() {
    echo -e "${CHECK} $1"
}

print_error() {
    echo -e "${CROSS} $1"
}

print_warning() {
    echo -e "${WARN} $1"
}

print_info() {
    echo -e "${INFO} $1"
}

check_command() {
    if command -v "$1" &> /dev/null; then
        return 0
    else
        return 1
    fi
}

##############################################################################
# MAIN INSTALLATION
##############################################################################

print_header

# Step 1: Check Python
print_step "Checking Python installation"

if check_command python3; then
    PYTHON_VERSION=$(python3 --version | grep -oP '\d+\.\d+')
    PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
    PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
        print_success "Python $PYTHON_VERSION found"
        PYTHON_CMD="python3"
    else
        print_error "Python 3.10+ required, found $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "Python 3 not found. Please install Python 3.10+"
    exit 1
fi

# Step 2: Check pip
print_step "Checking pip"

if check_command pip3; then
    print_success "pip found"
    PIP_CMD="pip3"
else
    print_error "pip not found. Please install pip"
    exit 1
fi

# Step 3: Create virtual environment
print_step "Creating virtual environment"

if [ -d "venv" ]; then
    print_warning "Virtual environment already exists, skipping creation"
else
    $PYTHON_CMD -m venv venv
    print_success "Virtual environment created"
fi

# Step 4: Activate virtual environment
print_step "Activating virtual environment"

source venv/bin/activate
print_success "Virtual environment activated"

# Step 5: Upgrade pip
print_step "Upgrading pip"

pip install --upgrade pip > /dev/null 2>&1
print_success "pip upgraded"

# Step 6: Install dependencies
print_step "Installing dependencies (this may take a few minutes)"

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Dependencies installed"
else
    print_error "requirements.txt not found"
    exit 1
fi

# Step 7: Check FFmpeg
print_step "Checking FFmpeg installation"

if check_command ffmpeg; then
    print_success "FFmpeg found"
else
    print_warning "FFmpeg not found. Download Manager will not work without it."
    print_info "Install FFmpeg:"
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "    sudo apt install ffmpeg  # Debian/Ubuntu"
        echo "    sudo yum install ffmpeg  # CentOS/RHEL"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "    brew install ffmpeg"
    fi
fi

# Step 8: Create .env file if not exists
print_step "Checking environment configuration"

if [ ! -f ".env" ]; then
    print_info "Creating .env file"
    cat > .env << EOF
# Django Settings
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Upload Settings
MAX_UPLOAD_SIZE=100
SUPPORTED_FORMATS=mp3,flac,ogg,m4a,wav

# Database (SQLite default)
DATABASE_URL=sqlite:///db.sqlite3

# Optional: Redis for caching (if installed)
# REDIS_URL=redis://127.0.0.1:6379/1
EOF
    print_success ".env file created"
else
    print_warning ".env file already exists, skipping"
fi

# Step 9: Run migrations
print_step "Setting up database"

python manage.py makemigrations
python manage.py migrate
print_success "Database migrations completed"

# Step 10: Create superuser
print_step "Creating superuser account"

echo -e "${INFO} You will be prompted to create an admin account"
echo -e "${INFO} Press Ctrl+C to skip if you already have one\n"

# Try to create superuser, but don't fail if cancelled
if python manage.py createsuperuser; then
    print_success "Superuser created"
else
    print_warning "Superuser creation skipped or failed"
fi

# Step 11: Collect static files
print_step "Collecting static files"

python manage.py collectstatic --noinput > /dev/null 2>&1
print_success "Static files collected"

# Step 12: Check for recommendation system migration
print_step "Checking recommendation engine setup"

if python manage.py showmigrations music | grep -q "ListeningHistory"; then
    print_success "Recommendation engine database ready"
else
    print_info "Recommendation engine migrations detected, applying..."
    python manage.py migrate music
    print_success "Recommendation engine ready"
fi

##############################################################################
# POST-INSTALL INFO
##############################################################################

echo -e ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✓ Installation Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e ""
echo -e "${BLUE}🚀 To start the server:${NC}"
echo -e ""
echo -e "  ${YELLOW}1.${NC} Activate virtual environment:"
echo -e "     ${GREEN}source venv/bin/activate${NC}"
echo -e ""
echo -e "  ${YELLOW}2.${NC} Run development server:"
echo -e "     ${GREEN}python manage.py runserver${NC}"
echo -e ""
echo -e "${BLUE}📍 Access points:${NC}"
echo -e ""
echo -e "  • Main App:          ${GREEN}http://localhost:8000${NC}"
echo -e "  • Download Manager:  ${GREEN}http://localhost:8000/music/downloads/${NC}"
echo -e "  • Admin Panel:       ${GREEN}http://localhost:8000/admin/${NC}"
echo -e "  • API Docs:          ${GREEN}http://localhost:8000/api/${NC}"
echo -e ""
echo -e "${BLUE}🤖 Recommendation System:${NC}"
echo -e ""
echo -e "  • Personalized:      ${GREEN}http://localhost:8000/music/api/recommendations/${NC}"
echo -e "  • Top Charts:        ${GREEN}http://localhost:8000/music/api/charts/${NC}"
echo -e "  • Continue Listening:${GREEN}http://localhost:8000/music/api/continue-listening/${NC}"
echo -e ""
if ! check_command ffmpeg; then
echo -e "${WARN} ${YELLOW}Don't forget to install FFmpeg for Download Manager!${NC}"
echo -e ""
fi
echo -e "${BLUE}📚 Documentation:${NC}"
echo -e ""
echo -e "  • README:               ${GREEN}README.md${NC}"
echo -e "  • Download Manager:     ${GREEN}docs/DOWNLOAD_QUICKSTART.md${NC}"
echo -e "  • Recommendations:      ${GREEN}docs/RECOMMENDATIONS.md${NC}"
echo -e "  • Steam UI:             ${GREEN}steam_ui/README.md${NC}"
echo -e ""
echo -e "${BLUE}💡 Tips:${NC}"
echo -e ""
echo -e "  • First time? Check ${GREEN}docs/DOWNLOAD_QUICKSTART.md${NC}"
echo -e "  • Need help? Open an issue on GitHub"
echo -e "  • Want to contribute? PRs welcome!"
echo -e ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e ""
echo -e "${GREEN}Happy streaming! 🎵${NC}"
echo -e ""
