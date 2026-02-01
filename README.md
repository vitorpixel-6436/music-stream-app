# 🎵 Music Stream App

**Django web application for music streaming and downloading with full metadata support**

Featuring the **Steam UI Framework** - a modular, reusable component library for beautiful gaming-inspired interfaces.

![Django](https://img.shields.io/badge/django-5.0-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## ✨ Features

### Music App
- 🎶 **Upload & Stream** - MP3, FLAC, OGG, M4A, WAV support
- 🎨 **Automatic Metadata** - Extract title, artist, album from files
- 🖼️ **Cover Art** - Automatic extraction or manual upload
- 🔍 **Search & Filter** - Find tracks quickly
- 📦 **Download** - Get your files back anytime
- 📊 **Admin Panel** - Full Django admin integration

### Steam UI Framework
- 🎭 **Glass Morphism** - Multi-layered frosted glass effects
- 🎮 **Steam Design** - Gaming-oriented dark theme
- 📦 **Modular Components** - Card, Carousel, Featured Banner
- 🔧 **Highly Customizable** - Configuration system
- 🚀 **Easy to Use** - Django template tags + Python API
- 📝 **Well Documented** - Full docs and examples
- ♻️ **Reusable** - Install in any Django project

---

## 📦 Installation

### 1. Clone Repository

```bash
git clone https://github.com/vitorpixel-6436/music-stream-app.git
cd music-stream-app
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit: **http://localhost:8000**

---

## 🎨 Steam UI Framework

This project includes **Steam UI Framework** - a standalone UI component library that can be used in any Django project.

### Quick Start with Steam UI

```django
{% load steam_ui %}

{% steam_css %}  <!-- Load styles -->

<!-- Use components -->
{% steam_featured featured_track %}
{% steam_carousel tracks title="Recent" %}
{% steam_card track %}

{% steam_js %}  <!-- Load scripts -->
```

### Install Steam UI in Other Projects

```bash
pip install git+https://github.com/vitorpixel-6436/music-stream-app.git
```

Add to `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'steam_ui',
]
```

### Documentation

- 📖 [**Steam UI README**](steam_ui/README.md) - Full component documentation
- 📝 [**Usage Examples**](USAGE_EXAMPLE.md) - Code examples and migration guide
- 🛠️ [**Components**](steam_ui/components.py) - Python API reference
- ⚙️ [**Configuration**](steam_ui/config.py) - Customization options

---

## 📁 Project Structure

```
music-stream-app/
├── config/                 # Django settings
├── music/                  # Main music app
│   ├── models.py           # Track, Artist models
│   ├── views.py            # Views and logic
│   ├── templates/          # HTML templates
│   └── static/             # Music app static files
├── steam_ui/               # 🎨 UI Framework (standalone package)
│   ├── __init__.py
│   ├── components.py       # Component classes
│   ├── config.py           # Configuration
│   ├── templatetags/       # Django template tags
│   ├── templates/          # Component templates
│   └── static/             # CSS & JS
├── media/                  # Uploaded files
├── setup.py                # Package setup
├── requirements.txt
└── manage.py
```

---

## 🛠️ Technology Stack

- **Backend:** Django 5.0
- **Database:** SQLite (default), PostgreSQL (production)
- **Frontend:** 
  - Steam UI Framework (custom)
  - Tailwind CSS
  - Alpine.js (lightweight)
- **Audio:** Mutagen (metadata extraction)
- **Deployment:** Docker ready

---

## 💻 Development

### Run Tests

```bash
python manage.py test
```

### Collect Static Files

```bash
python manage.py collectstatic
```

### Create Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🌐 Environment Variables

Create `.env` file:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
MAX_UPLOAD_SIZE=100
SUPPORTED_FORMATS=mp3,flac,ogg,m4a,wav
```

---

## 🚀 Deployment

### Docker

```bash
docker-compose up -d
```

### Production Settings

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECURE_SSL_REDIRECT = True
```

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

MIT License - feel free to use this project and Steam UI Framework in your own work!

---

## 🔗 Links

- [Live Demo](#) (coming soon)
- [Issue Tracker](https://github.com/vitorpixel-6436/music-stream-app/issues)
- [Steam UI Docs](steam_ui/README.md)
- [Usage Examples](USAGE_EXAMPLE.md)

---

## ⭐ Features Roadmap

- [ ] User authentication
- [ ] Playlists
- [ ] Lyrics integration
- [ ] Social features
- [ ] Mobile app (React Native)
- [x] **Steam UI Framework** ✅
- [x] Glass morphism effects ✅
- [x] Responsive design ✅

---

**Made with ❤️ by vitorpixel-6436**

*Featuring Steam UI Framework - A modular component library for Django*
