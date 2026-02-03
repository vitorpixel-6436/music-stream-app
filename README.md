# 🎵 Music Stream App

**Django web application for music streaming and downloading with ML-powered recommendations**

Featuring the **Steam UI Framework** - a modular, reusable component library for beautiful gaming-inspired interfaces.

![Django](https://img.shields.io/badge/django-6.0-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Version](https://img.shields.io/badge/version-1.3.0-orange)
![License](https://img.shields.io/badge/license-MIT-purple)

---

## ✨ Features

### Music App
- 🎶 **Upload & Stream** - MP3, FLAC, OGG, M4A, WAV support
- 📥 **Download Manager** - Import from YouTube, SoundCloud, Bandcamp
- 🤖 **ML Recommendations** ⭐ NEW! - Personalized music recommendations
- 📊 **Real-time Progress** - Live download tracking with progress bars
- 🎨 **Automatic Metadata** - Extract title, artist, album from files
- 🖼️ **Cover Art** - Automatic extraction or manual upload
- 🔍 **Search & Filter** - Find tracks quickly
- 📦 **Export** - Get your files back anytime
- 📊 **Admin Panel** - Full Django admin integration

### ML Recommendation Engine ⭐ NEW! (v1.3.0)
- 🧠 **Content-Based Filtering** - Similar tracks by genre, artist, metadata
- 👥 **Collaborative Filtering** - Based on user listening patterns
- 📈 **Top Charts** - Weekly/monthly trending tracks
- ⏯️ **Continue Listening** - Resume incomplete tracks
- 📊 **Listening Stats** - Track your music habits
- ⚡ **No External Dependencies** - Pure Python + Django ORM
- 🚀 **Fast** - <100ms response time with caching
- 🎯 **7 REST API Endpoints** - Easy frontend integration

### Download Manager
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

### ⚡ Automatic Installation (Recommended)

#### Linux/macOS:

```bash
# 1. Clone repository
git clone https://github.com/vitorpixel-6436/music-stream-app.git
cd music-stream-app

# 2. Run automatic installer
chmod +x install.sh
./install.sh

# 3. Start server
source venv/bin/activate
python manage.py runserver
```

#### Windows:

```cmd
REM 1. Clone repository
git clone https://github.com/vitorpixel-6436/music-stream-app.git
cd music-stream-app

REM 2. Run automatic installer (double-click or run in cmd)
install.bat

REM 3. Start server
venv\Scripts\activate
python manage.py runserver
```

**That's it! 🎉** The installer handles:
- ✅ Virtual environment creation
- ✅ Dependency installation
- ✅ Database setup and migrations
- ✅ Superuser creation
- ✅ Static files collection
- ✅ Recommendation engine setup

---

### 📋 Manual Installation

<details>
<summary>Click to expand manual installation steps</summary>

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

#### 6. Collect Static Files

```bash
python manage.py collectstatic
```

#### 7. Run Development Server

```bash
python manage.py runserver
```

</details>

---

## 🌐 Access Points

After installation, visit:

| Feature | URL |
|---------|-----|
| **Main App** | http://localhost:8000 |
| **Download Manager** | http://localhost:8000/music/downloads/ |
| **Admin Panel** | http://localhost:8000/admin/ |
| **API Root** | http://localhost:8000/api/ |

### 🤖 Recommendation API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/recommendations/` | Personalized recommendations |
| `/api/track/<id>/similar/` | Similar tracks |
| `/api/charts/` | Top charts (weekly/monthly) |
| `/api/continue-listening/` | Resume listening |
| `/api/track/<id>/play/` | Record play event |
| `/api/listening-stats/` | User statistics |
| `/api/recent-plays/` | Recent play history |

---

## 📚 Documentation

### Core Documentation
- 📖 [**Installation Guide**](INSTALL.md) - Detailed setup instructions
- 📝 [**Usage Examples**](USAGE_EXAMPLE.md) - Code examples

### Feature Documentation
- 🤖 [**Recommendation Engine**](docs/RECOMMENDATIONS.md) ⭐ - ML algorithms & API reference
- 📥 [**Download Manager Quick Start**](docs/DOWNLOAD_QUICKSTART.md) - 5-minute guide
- 📥 [**Download Manager Setup**](docs/DOWNLOAD_SETUP.md) - Full configuration
- 📥 [**Download API Reference**](docs/DOWNLOAD_API.md) - REST API docs

### UI Framework
- 🎨 [**Steam UI README**](steam_ui/README.md) - Component documentation
- 🔧 [**Components API**](steam_ui/components.py) - Python reference
- ⚙️ [**Configuration**](steam_ui/config.py) - Customization options

---

## 🤖 Using the Recommendation Engine

### Python API

```python
from music.recommendations import RecommendationEngine

engine = RecommendationEngine()

# Get personalized recommendations
recommendations = engine.get_personalized_recommendations(
    user=request.user,
    limit=20
)

# Get similar tracks
similar = engine.get_similar_tracks(
    track=my_track,
    limit=10
)

# Get top charts
charts = engine.get_top_charts(
    period_days=7,  # Weekly
    limit=20
)
```

### REST API

```bash
# Personalized recommendations
curl http://localhost:8000/music/api/recommendations/

# Top charts (weekly)
curl http://localhost:8000/music/api/charts/?period=weekly

# Similar tracks
curl http://localhost:8000/music/api/track/<id>/similar/

# Record play event
curl -X POST http://localhost:8000/music/api/track/<id>/play/ \
  -H "Content-Type: application/json" \
  -d '{"duration": 180, "position": 180}'
```

### Frontend Integration

```html
<!-- Include CSS & JS -->
<link rel="stylesheet" href="{% static 'music/css/recommendations.css' %}">
<script src="{% static 'music/js/recommendations.js' %}" defer></script>

<!-- Add containers -->
<div id="personalized-recommendations"></div>
<div id="top-charts"></div>
<div id="continue-listening"></div>
```

The JavaScript automatically loads and displays recommendations with Steam UI styling.

---

## 🎨 Steam UI Framework - Standalone Installation

This project includes **Steam UI Framework** - a standalone UI component library that can be installed in any Django project.

### 🚀 Quick Install (Multiple Options)

#### Option 1: Install from ZIP (⭐ Recommended - No Git Required)

```bash
pip install https://github.com/vitorpixel-6436/music-stream-app/archive/refs/heads/main.zip
```

#### Option 2: Install from GitHub Release

```bash
pip install https://github.com/vitorpixel-6436/music-stream-app/releases/download/v1.3.0/steam_ui_framework-1.3.0-py3-none-any.whl
```

#### Option 3: Install with Git

```bash
pip install git+https://github.com/vitorpixel-6436/music-stream-app.git
```

### Using Steam UI Framework

Add to `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'steam_ui',
]
```

Template usage:
```django
{% load steam_ui %}

{% steam_css %}
{% steam_featured featured_track %}
{% steam_carousel tracks title="Recent" icon="fa-clock" %}
{% steam_js %}
```

---

## 🐛 Troubleshooting

### Installation Issues

**Problem:** Python not found  
**Solution:** Install Python 3.10+ from [python.org](https://www.python.org/downloads/)

**Problem:** FFmpeg not found  
**Solution:** 
- Windows: `choco install ffmpeg`
- Linux: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`

**Problem:** Permission denied on `install.sh`  
**Solution:** `chmod +x install.sh`

### Runtime Issues

**Problem:** Static files not loading  
**Solution:** `python manage.py collectstatic`

**Problem:** Recommendations not showing  
**Solution:** Make sure migrations are applied: `python manage.py migrate`

**Full troubleshooting:** See [INSTALL.md](INSTALL.md) or [docs/RECOMMENDATIONS.md](docs/RECOMMENDATIONS.md)

---

## 📁 Project Structure

```
music-stream-app/
├── config/                     # Django settings
├── music/                      # Main music app
│   ├── models.py               # Track, Artist, DownloadTask, ListeningHistory
│   ├── views.py                # Views and logic
│   ├── download_views.py       # Download manager views
│   ├── recommendation_views.py # Recommendation API ⭐ NEW!
│   ├── recommendations.py      # ML engine ⭐ NEW!
│   ├── downloaders.py          # yt-dlp integration
│   ├── tasks.py                # Background processing
│   ├── templates/              # HTML templates
│   └── static/                 # CSS, JS
│       ├── css/
│       │   └── recommendations.css  # ⭐ NEW!
│       └── js/
│           └── recommendations.js   # ⭐ NEW!
├── steam_ui/                   # 🎨 UI Framework (standalone)
│   ├── components.py
│   ├── templatetags/
│   ├── templates/
│   └── static/
├── docs/                       # Documentation
│   ├── RECOMMENDATIONS.md      # ⭐ NEW! ML engine docs
│   ├── DOWNLOAD_QUICKSTART.md
│   ├── DOWNLOAD_SETUP.md
│   └── DOWNLOAD_API.md
├── install.sh                  # ⭐ NEW! Linux/Mac installer
├── install.bat                 # ⭐ NEW! Windows installer
├── setup.py                    # Package setup
├── requirements.txt
└── manage.py
```

---

## 🛠️ Technology Stack

- **Backend:** Django 6.0, Python 3.10+
- **Database:** SQLite (default), PostgreSQL (production)
- **ML Engine:** Pure Python (TF-IDF, Cosine Similarity) ⭐
- **Frontend:** 
  - Steam UI Framework (custom)
  - Vanilla JavaScript
  - CSS3 with Glass Morphism
- **Audio:** 
  - Mutagen (metadata extraction)
  - FFmpeg (audio conversion)
  - yt-dlp (YouTube/SoundCloud downloads)
- **Task Processing:** Threading (upgradeable to Celery)
- **Caching:** Django cache framework (Redis optional)
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

### Create Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🌐 Environment Variables

Create `.env` file (automatically created by installer):

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
MAX_UPLOAD_SIZE=100
SUPPORTED_FORMATS=mp3,flac,ogg,m4a,wav

# Optional: Redis for caching
# REDIS_URL=redis://127.0.0.1:6379/1
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

# Use Redis for caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
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

- [Issue Tracker](https://github.com/vitorpixel-6436/music-stream-app/issues)
- [Releases](https://github.com/vitorpixel-6436/music-stream-app/releases)
- [Documentation](docs/)

---

## ⭐ Features Roadmap

### Completed ✅
- [x] **Steam UI Framework** ✅
- [x] Glass morphism effects ✅
- [x] Responsive design ✅
- [x] **Player Bar component** ✅ (v1.1.0)
- [x] **Playlist component** ✅ (v1.1.0)
- [x] **Download Manager** ✅ (v1.2.0)
- [x] Real-time progress tracking ✅
- [x] YouTube/SoundCloud support ✅
- [x] **ML Recommendation Engine** ✅ (v1.3.0) ⭐ NEW!
- [x] Personalized recommendations ✅
- [x] Listening history tracking ✅
- [x] **Automatic Installers** ✅ (v1.3.0) ⭐ NEW!

### In Progress 🚧
- [ ] Playlists functionality
- [ ] User authentication improvements

### Planned 📋
- [ ] Advanced ML models (deep learning)
- [ ] Lyrics integration
- [ ] Social features (sharing, following)
- [ ] Mobile app (React Native)
- [ ] Audio editor/mixer
- [ ] Spotify/Apple Music import

---

## 📊 Version History

### v1.3.0 (Latest) ⭐ NEW!
- 🤖 **ML-Powered Recommendation Engine**
  - Content-based filtering
  - Collaborative filtering
  - TF-IDF + Cosine similarity (pure Python)
  - 7 REST API endpoints
  - Listening history tracking
  - Top charts (weekly/monthly)
  - Continue listening feature
- 🚀 **Automatic Installers**
  - One-command installation for Linux/Mac (`install.sh`)
  - One-click installation for Windows (`install.bat`)
  - Auto-setup database, migrations, static files
- 📝 **Comprehensive Documentation**
  - [Recommendation Engine Guide](docs/RECOMMENDATIONS.md)
  - API reference with examples
  - Frontend integration instructions

### v1.2.0
- ✨ **Download Manager** - Import from YouTube, SoundCloud, Bandcamp
- 📊 Real-time progress tracking
- 🔄 Auto-retry on failure
- 🎵 Multiple format support

### v1.1.0
- ✨ Added `PlayerBar` component
- ✨ Added `Playlist` component  
- 🔧 Improved package distribution

### v1.0.0
- 🎉 Initial release
- ✨ Core components: Card, Carousel, Featured Banner
- 🎨 Glass morphism styling

---

**Made with ❤️ by vitorpixel-6436**

*Featuring:*
- *Steam UI Framework - A modular component library for Django*
- *ML Recommendation Engine - Personalized music discovery* ⭐ NEW!
- *Download Manager - Import music from anywhere*

**Quick Start:**
```bash
git clone https://github.com/vitorpixel-6436/music-stream-app.git
cd music-stream-app
./install.sh  # Linux/Mac
# or
install.bat   # Windows
```

**Need Help?**
- 📖 [Installation Guide](INSTALL.md)
- 🤖 [Recommendation Docs](docs/RECOMMENDATIONS.md) ⭐
- 📥 [Download Manager Guide](docs/DOWNLOAD_QUICKSTART.md)
- 🐛 [Open an Issue](https://github.com/vitorpixel-6436/music-stream-app/issues)
