# 🚀 Installation Guide - Music Stream App with Steam UI

## 💻 System Requirements

- **Python:** 3.10 or higher
- **pip:** Latest version
- **Database:** SQLite (included) or PostgreSQL
- **OS:** Linux, macOS, Windows
- **RAM:** 512MB minimum (2GB recommended)
- **Disk Space:** 1GB minimum

---

## 📦 Quick Installation (5 minutes)

### 1. Clone & Navigate

```bash
git clone https://github.com/vitorpixel-6436/music-stream-app.git
cd music-stream-app
```

### 2. Create Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Setup Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

*Follow prompts to create admin account*

### 5. Run Server

```bash
python manage.py runserver
```

**✅ Done!** Visit: http://localhost:8000

**Admin Panel:** http://localhost:8000/admin

---

## ⚙️ Environment Configuration

### Create `.env` file

```bash
cp .env.example .env  # Or create manually
```

### Basic Configuration

```env
# Security
SECRET_KEY=django-insecure-please-change-this-1234567890abcdef
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database (optional - defaults to SQLite)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# File Upload
MAX_UPLOAD_SIZE=100  # in MB
SUPPORTED_FORMATS=mp3,flac,ogg,m4a,wav

# Language & Timezone
LANGUAGE_CODE=en-us
TIME_ZONE=UTC

# CORS (for API access)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Generate Secret Key

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## 🔧 Development Setup

### Install Development Tools

```bash
pip install -r requirements-dev.txt  # if exists
pip install pytest pytest-django black flake8
```

### Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Run Tests

```bash
python manage.py test
pytest  # alternative
```

### Create Test Data

```bash
python manage.py loaddata fixtures/test_data.json
```

---

## 🐟 Docker Deployment

### Using Docker Compose

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## 🌐 Production Deployment

### Security Checklist

- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Set up CSRF protection
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets

### Production Settings

```python
# config/settings.py

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'music_db',
        'USER': 'music_user',
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static and Media
STATIC_ROOT = '/var/www/music-app/static/'
MEDIA_ROOT = '/var/www/music-app/media/'

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Deploy with Gunicorn + Nginx

**1. Install Gunicorn:**
```bash
pip install gunicorn
```

**2. Test Gunicorn:**
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

**3. Create systemd service** (`/etc/systemd/system/music-app.service`):
```ini
[Unit]
Description=Music Stream App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/music-app
Environment="PATH=/var/www/music-app/venv/bin"
ExecStart=/var/www/music-app/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/music-app.sock \
    config.wsgi:application

[Install]
WantedBy=multi-user.target
```

**4. Configure Nginx** (`/etc/nginx/sites-available/music-app`):
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/music-app/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/music-app/media/;
    }

    location / {
        proxy_pass http://unix:/run/music-app.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**5. Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl start music-app
sudo systemctl enable music-app
sudo systemctl restart nginx
```

---

## 📚 Database Migration (SQLite → PostgreSQL)

### 1. Export data from SQLite
```bash
python manage.py dumpdata > backup.json
```

### 2. Update settings to PostgreSQL
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'music_db',
        'USER': 'music_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Create new database
```bash
psql -U postgres
CREATE DATABASE music_db;
CREATE USER music_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE music_db TO music_user;
\q
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Import data
```bash
python manage.py loaddata backup.json
```

---

## 🔍 Troubleshooting

### Issue: Port 8000 already in use
```bash
# Use different port
python manage.py runserver 8001

# Or kill process
lsof -ti:8000 | xargs kill -9  # Linux/Mac
netstat -ano | findstr :8000   # Windows
```

### Issue: Static files not loading
```bash
python manage.py collectstatic --clear
python manage.py collectstatic
```

### Issue: Database locked (SQLite)
```bash
# Close all connections
pkill -f manage.py

# Or delete db.sqlite3 and migrate again
rm db.sqlite3
python manage.py migrate
```

### Issue: Permission denied on media files
```bash
sudo chown -R www-data:www-data /var/www/music-app/media/
sudo chmod -R 755 /var/www/music-app/media/
```

### Issue: Steam UI components not showing
1. Check `INSTALLED_APPS` includes `'steam_ui'`
2. Run `collectstatic`
3. Clear browser cache
4. Check browser console for errors

---

## 🎨 Installing Steam UI Only

If you only want the Steam UI Framework:

```bash
pip install git+https://github.com/vitorpixel-6436/music-stream-app.git
```

Add to your Django project:
```python
INSTALLED_APPS = [
    ...
    'steam_ui',
]

STATICFILES_DIRS = [
    BASE_DIR / 'steam_ui' / 'static',
]
```

See [Steam UI README](steam_ui/README.md) for full documentation.

---

## 🔗 Additional Resources

- [Main README](README.md) - Project overview
- [Usage Examples](USAGE_EXAMPLE.md) - Code examples
- [Steam UI Docs](steam_ui/README.md) - Component documentation
- [Django Docs](https://docs.djangoproject.com/) - Django reference

---

## ❓ Need Help?

- [Open an Issue](https://github.com/vitorpixel-6436/music-stream-app/issues)
- [Discussions](https://github.com/vitorpixel-6436/music-stream-app/discussions)

---

**Happy streaming! 🎵**
