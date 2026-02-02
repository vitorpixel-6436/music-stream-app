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
- 📥 **Download Manager** ⭐ NEW! - Import from YouTube, SoundCloud, Bandcamp
- 📊 **Real-time Progress** - Live download tracking with progress bars
- 🎨 **Automatic Metadata** - Extract title, artist, album from files
- 🖼️ **Cover Art** - Automatic extraction or manual upload
- 🔍 **Search & Filter** - Find tracks quickly
- 📦 **Export** - Get your files back anytime
- 📊 **Admin Panel** - Full Django admin integration

### Download Manager ⭐ NEW!
- 🌐 **Multiple Sources** - YouTube, SoundCloud, Bandcamp, Direct URLs
- 📈 **Live Progress Tracking** - Real-time progress bars (0-100%)
- 🔄 **Auto-retry** - Up to 3 automatic retry attempts
- 🎵 **Format Conversion** - MP3, FLAC, OGG, M4A, WAV output
- 🎛️ **Quality Control** - 320k, 256k, 192k, 128k bitrates
- 🧵 **Background Processing** - Non-blocking, threaded downloads
- 📝 **Auto Metadata** - Automatic title, artist, album extraction
- 🎨 **Beautiful UI** - Steam-inspired design with live updates

### Steam UI Framework
- 🎭 **Glass Morphism** - Multi-layered frosted glass effects
- 🎮 **Steam Design** - Gaming-oriented dark theme
- 📦 **Modular Components** - Card, Carousel, Featured Banner, Player Bar, Playlist
- 🔧 **Highly Customizable** - Configuration system
- 🚀 **Easy to Use** - Django template tags + Python API
- 📝 **Well Documented** - Full docs and examples
- ♻️ **Reusable** - Install in any Django project

---

## 🚀 Quick Start

### Full App Installation

#### 1. Clone Repository

```bash
git clone https://github.com/vitorpixel-6436/music-stream-app.git
cd music-stream-app
```

#### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Install FFmpeg (Required for Download Manager)

**Windows:**
```bash
choco install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

#### 5. Setup Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

#### 6. Run Development Server

```bash
python manage.py runserver
```

Visit: 
- **Main App:** http://localhost:8000
- **Download Manager:** http://localhost:8000/music/downloads/

### ⚡ Download Manager Quick Start

**New to Download Manager?**

👉 [**5-Minute Quick Start Guide**](docs/DOWNLOAD_QUICKSTART.md) ⭐

---

## 📥 Download Manager Documentation

### Getting Started

1. **[Quick Start (5 min)](docs/DOWNLOAD_QUICKSTART.md)** ⭐ - Your first download
2. **[Full Setup Guide](docs/DOWNLOAD_SETUP.md)** - Detailed configuration
3. **[API Reference](docs/DOWNLOAD_API.md)** - REST API documentation

### Features in Detail

```python
# Example: Download from YouTube
from music.models import DownloadTask
from django.contrib.auth.models import User

user = User.objects.first()
task = DownloadTask.objects.create(
    user=user,
    url='https://www.youtube.com/watch?v=jNQXAC9IVRw',
    output_format='mp3',
    output_quality='320k',
    source_type='youtube'
)

# Processing starts automatically!
print(f"Progress: {task.progress}%")  # Live updates
print(f"Status: {task.status}")        # pending → downloading → completed
```

### Web Interface

- **Create Downloads:** `/music/downloads/create/`
- **Monitor Progress:** `/music/downloads/`
- **Status API:** `/music/api/downloads/<id>/status/`

---

## 🎨 Steam UI Framework - Standalone Installation

This project includes **Steam UI Framework** - a standalone UI component library that can be installed in any Django project.

### 🚀 Quick Install (Multiple Options)

#### Option 1: Install from ZIP (⭐ Recommended - No Git Required)

**For users without Git installed:**

```bash
pip install https://github.com/vitorpixel-6436/music-stream-app/archive/refs/heads/main.zip
```

#### Option 2: Install from GitHub Release (No Git Required)

```bash
# Download wheel from Releases page, then:
pip install steam_ui_framework-1.1.0-py3-none-any.whl

# Or install directly from URL:
pip install https://github.com/vitorpixel-6436/music-stream-app/releases/download/v1.1.0/steam_ui_framework-1.1.0-py3-none-any.whl
```

#### Option 3: Install with Git

**If you have Git installed:**

```bash
pip install git+https://github.com/vitorpixel-6436/music-stream-app.git
```

#### Option 4: Install from PyPI (Coming Soon)

```bash
pip install steam-ui-framework
```

### 📚 Detailed Installation Guide

**Having trouble?** See [**INSTALL.md**](INSTALL.md) for:
- Step-by-step instructions
- Building from source
- Troubleshooting
- Platform-specific guides

---

## 🎮 Using Steam UI Framework

### Django Setup

Add to `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'steam_ui',
]
```

### Template Usage

```django
{% load steam_ui %}

<!-- Load styles and scripts -->
{% steam_css %}

<!-- Use components -->
{% steam_featured featured_track %}
{% steam_carousel tracks title="Recent" icon="fa-clock" %}
{% steam_card track %}
{% steam_player_bar current_track %}
{% steam_playlist playlist %}

{% steam_js %}
```

### Python Usage

```python
from steam_ui import Card, Carousel, PlayerBar, Playlist

# Create components
card = Card(show_actions=True, size='normal')
html = card.render(track=my_track)

player = PlayerBar(autoplay=False)
player_html = player.render(current_track=track)
```

### Documentation

- 📖 [**Steam UI README**](steam_ui/README.md) - Full component documentation
- 📝 [**Usage Examples**](USAGE_EXAMPLE.md) - Code examples and migration guide  
- 🔧 [**Installation Guide**](INSTALL.md) - Detailed installation instructions
- 🛠️ [**Components**](steam_ui/components.py) - Python API reference
- ⚙️ [**Configuration**](steam_ui/config.py) - Customization options

---

## 🐛 Troubleshooting

### "Cannot find command 'git'" Error

**Problem:** Git is not installed on your system.

**Solutions:**
1. **Use Option 1 or 2 above** (No Git required) ⭐
2. Install Git from [git-scm.com](https://git-scm.com/downloads)
3. See [INSTALL.md](INSTALL.md) for more details

### Package Installation Issues

```bash
# Update pip first
python -m pip install --upgrade pip

# Then try installation again
pip install https://github.com/vitorpixel-6436/music-stream-app/archive/refs/heads/main.zip
```

### Static Files Not Loading

```bash
python manage.py collectstatic
```

### Download Manager Issues

See [**Download Manager Troubleshooting**](docs/DOWNLOAD_SETUP.md#troubleshooting)

**Full troubleshooting guide:** [INSTALL.md](INSTALL.md)

---

## 📁 Project Structure

```
music-stream-app/
├── config/                 # Django settings
├── music/                  # Main music app
│   ├── models.py           # Track, Artist, DownloadTask models
│   ├── views.py            # Views and logic
│   ├── download_views.py   # Download manager views ⭐ NEW!
│   ├── downloaders.py      # yt-dlp integration ⭐ NEW!
│   ├── tasks.py            # Background processing ⭐ NEW!
│   ├── templates/          # HTML templates
│   └── static/             # Music app static files
├── steam_ui/               # 🎨 UI Framework (standalone package)
│   ├── __init__.py
│   ├── components.py       # Component classes
│   ├── config.py           # Configuration
│   ├── templatetags/       # Django template tags
│   ├── templates/          # Component templates
│   └── static/             # CSS & JS
├── docs/                   # Documentation
│   ├── DOWNLOAD_QUICKSTART.md  # ⭐ 5-minute guide
│   ├── DOWNLOAD_SETUP.md       # Full setup
│   └── DOWNLOAD_API.md         # API reference
├── media/                  # Uploaded files
├── setup.py                # Package setup
├── build_package.py        # Build automation
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
- **Audio:** 
  - Mutagen (metadata extraction)
  - FFmpeg (audio conversion)
  - yt-dlp (YouTube/SoundCloud downloads) ⭐
- **Task Processing:** Threading (upgradeable to Celery)
- **Deployment:** Docker ready

---

## 💻 Development

### Run Tests

```bash
python manage.py test
```

### Build Package

```bash
python build_package.py
```

This creates:
- `dist/steam_ui_framework-1.1.0-py3-none-any.whl`
- `dist/steam-ui-framework-1.1.0.tar.gz`

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
- [Installation Guide](INSTALL.md) ⭐
- [Download Manager Quick Start](docs/DOWNLOAD_QUICKSTART.md) ⭐ NEW!
- [Usage Examples](USAGE_EXAMPLE.md)

---

## ⭐ Features Roadmap

### Completed ✅
- [x] **Steam UI Framework** ✅
- [x] Glass morphism effects ✅
- [x] Responsive design ✅
- [x] **Player Bar component** ✅ (v1.1.0)
- [x] **Playlist component** ✅ (v1.1.0)
- [x] **Git-free installation** ✅
- [x] **Download Manager** ✅ (v1.2.0) ⭐ NEW!
- [x] Real-time progress tracking ✅
- [x] YouTube/SoundCloud support ✅

### In Progress 🚧
- [ ] Playlists functionality
- [ ] ML-based recommendations

### Planned 📋
- [ ] User authentication
- [ ] Lyrics integration
- [ ] Social features
- [ ] Mobile app (React Native)
- [ ] Audio editor/mixer

---

## 📊 Version History

### v1.2.0 (Latest) ⭐
- ✨ **Download Manager** - Import from YouTube, SoundCloud, Bandcamp
- 📊 Real-time progress tracking
- 🔄 Auto-retry on failure
- 🎵 Multiple format support (MP3, FLAC, OGG, M4A, WAV)
- 🎨 Beautiful Steam-inspired UI
- 📝 Comprehensive documentation (3 guides)

### v1.1.0
- ✨ Added `PlayerBar` component (floating audio player)
- ✨ Added `Playlist` component  
- 🔧 Improved package distribution
- 📝 Added comprehensive installation guide
- 🐛 Fixed Git dependency issues

### v1.0.0
- 🎉 Initial release
- ✨ Core components: Card, Carousel, Featured Banner
- 🎨 Glass morphism styling
- 📦 Django template tags

---

**Made with ❤️ by vitorpixel-6436**

*Featuring:*
- *Steam UI Framework - A modular component library for Django*
- *Download Manager - Import music from anywhere* ⭐ NEW!

**Getting Started:**
- **App Installation:** See above ⬆️
- **Download Manager:** [5-Minute Quick Start](docs/DOWNLOAD_QUICKSTART.md) ⭐
- **Having issues?** [INSTALL.md](INSTALL.md) or [open an issue](https://github.com/vitorpixel-6436/music-stream-app/issues)
