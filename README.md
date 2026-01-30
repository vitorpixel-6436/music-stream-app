# 🎵 Music Stream App

**Premium music streaming application** с четырьмя UI дизайн-системами: Apple Glass Effects, Steam Gaming Cards, Spotify Minimalism, и MSI Gaming Vibes.

![Version](https://img.shields.io/badge/version-2.1.1-red.svg)
![Django](https://img.shields.io/badge/django-6.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![UI Components](https://img.shields.io/badge/UI_components-108KB-orange.svg)

---

## ✨ Features

### 🎵 Core Functionality
- ✅ Music upload (MP3, FLAC, WAV, M4A, OGG)
- ✅ Bulk upload with drag-and-drop
- ✅ **URL import from YouTube/SoundCloud**
- ✅ **Background download queue**
- ✅ High-quality audio streaming
- ✅ Cover image support
- ✅ Automatic metadata extraction
- ✅ Search & filtering
- ✅ Download tracks
- ✅ Responsive player interface
- ✅ Progressive Web App (PWA)

### 🛠️ Admin & Management
- ✅ Enhanced admin panel with rich UI
- ✅ System settings web interface
- ✅ Management commands (`addadmin`, `update_stats`)
- ✅ Upload session tracking
- ✅ **Download task monitoring**
- ✅ Real-time statistics dashboard
- ✅ Bulk metadata extraction
- ✅ Audio preview in admin
- ✅ Color-coded badges and progress bars

### 🎨 Design Systems

#### 1. **Apple Glass Effects** (37.1 KB)
- Liquid glass morphism with backdrop-filter blur
- Dynamic glass layers (layer-1, layer-2, layer-3)
- Context-aware blur adjustments
- Scroll-reactive elevations
- Hover depth effects
- Floating particle animations
- Specular highlights & edge lighting

#### 2. **Steam Gaming Cards** (35.2 KB)
- Grid cards with 3:4 aspect ratio
- Interactive carousels with drag-to-scroll
- Featured hero banners (21:9 format)
- Quick action buttons (like, playlist, download)
- Play overlays with 80px circular buttons
- Category pills with horizontal scrolling
- Progress tracking & keyboard navigation

#### 3. **Spotify Minimalism** (23.0 KB)
- Sticky navigation with scroll reveal
- Browser history integration (back/forward)
- Breadcrumb navigation
- Compact sidebar with hover expand (72px → 280px)
- Minimal cards with green play button (#1db954)
- Pill filters & icon buttons
- Smooth page transitions
- Ctrl+K search shortcut

#### 4. **MSI Gaming Vibes** (13.0 KB)
- RGB glow animations
- Angular clip-path designs
- Performance stats widgets
- Neon red accents with pulse effects
- Hexagon background patterns
- Dragon-themed accents
- Scanline CRT effects
- Gaming-style buttons & inputs

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Django 6.0+
- Redis (for background tasks)
- ffmpeg (for audio conversion)
- Modern browser with backdrop-filter support

### Installation

```bash
# Clone repository
git clone https://github.com/vitorpixel-6436/music-stream-app.git
cd music-stream-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin user
python manage.py addadmin admin@example.com --superuser

# Update statistics
python manage.py update_stats

# Start Redis (in separate terminal)
redis-server

# Start Celery worker (in separate terminal)
celery -A music_stream worker -l info

# Run development server
python manage.py runserver
```

### Access
- **App**: http://localhost:8000/
- **Admin**: http://localhost:8000/admin/
- **Upload**: http://localhost:8000/upload/
- **URL Import**: http://localhost:8000/import/
- **Downloads**: http://localhost:8000/downloads/

---

## 🎯 Management Commands

### Quick Admin Creation
```bash
# Create superuser
python manage.py addadmin admin@example.com --superuser

# Create staff user
python manage.py addadmin user@example.com --username myuser

# Promote existing user
python manage.py addadmin existing@example.com --superuser
```

### Update Statistics
```bash
# Refresh system statistics
python manage.py update_stats
```

---

## 🎯 Project Structure

```
music-stream-app/
├── music/
│   ├── management/
│   │   └── commands/
│   │       ├── addadmin.py          # Quick admin creation
│   │       └── update_stats.py      # Statistics updater
│   │
│   ├── migrations/
│   │   ├── 0002_system_settings.py  # v2.1.0 models
│   │   └── 0003_download_task.py    # v2.1.1 download tasks
│   │
│   ├── utils/
│   │   └── downloader.py        # Media download helper
│   │
│   ├── static/
│   │   ├── css/
│   │   │   ├── glass-liquid.css        # Apple glass (13.0 KB)
│   │   │   ├── glass-dynamics.css      # Dynamic effects (10.7 KB)
│   │   │   ├── steam-cards.css         # Gaming cards (12.9 KB)
│   │   │   ├── steam-carousel.css      # Carousels (9.9 KB)
│   │   │   ├── spotify-minimal.css     # Minimalism (10.6 KB)
│   │   │   └── msi-gaming.css          # Gaming vibes (13.0 KB)
│   │   │
│   │   └── js/
│   │       ├── glass-dynamics.js       # Glass system (13.4 KB)
│   │       ├── steam-carousel.js       # Carousel logic (12.4 KB)
│   │       └── spotify-minimal.js      # Spotify UI (12.4 KB)
│   │
│   ├── templates/music/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── upload.html
│   │   ├── url_import.html          # URL import page
│   │   └── download_manager.html    # Download queue
│   │
│   ├── models.py              # Includes DownloadTask
│   ├── admin.py               # Enhanced admin interface
│   ├── views.py               # Includes URL import views
│   ├── tasks.py               # Celery background tasks
│   ├── forms.py               # Includes URLImportForm
│   ├── consumers.py           # WebSocket consumers
│   └── urls.py
│
├── CHANGELOG.md               # Version history
├── COMPONENTS.md              # UI documentation (16.9 KB)
├── README.md                  # This file
├── requirements.txt
└── manage.py
```

---

## 💻 Tech Stack

### Backend
- **Django 6.0** - Web framework
- **Celery** - Asynchronous task queue
- **Redis** - Cache and message broker
- **yt-dlp** - YouTube/media downloader
- **ffmpeg-python** - Audio conversion
- **Pillow** - Image processing
- **Mutagen** - Audio metadata extraction
- **Python 3.10+** - Programming language

### Frontend
- **Tailwind CSS** - Utility-first CSS framework
- **Font Awesome 6.5** - Icon library
- **Inter & Orbitron** - Google Fonts
- **Vanilla JavaScript** - No dependencies

### UI Systems
- **Glass Morphism** - backdrop-filter, blur effects
- **Clip-path** - Angular gaming designs
- **CSS Grid** - Responsive layouts
- **CSS Animations** - RGB glows, neon pulses
- **Intersection Observer** - Fade-in animations
- **History API** - Browser navigation

---

## 📝 Release Notes

### Version 2.1.1 (2026-01-30) - Server-Side Downloads

#### ✨ New Features
- ✅ **URL Import System** - Download from YouTube, SoundCloud, Bandcamp
- ✅ **DownloadTask Model** - Track download progress and status
- ✅ **Background Queue** - Celery-based async download processing
- ✅ **Download Manager** - Web interface for task monitoring
- ✅ **Format Conversion** - Auto-convert to MP3/FLAC with quality settings
- ✅ **Error Handling** - Retry mechanisms and detailed error logs

#### 🔧 Improvements
- Enhanced form validation for URLs
- Optimized database queries with indexes
- Background task optimization
- Better error reporting

### Version 2.1.0 (2026-01-30) - Admin & Management QoL

#### ✨ New Features
- ✅ **SystemSettings Model** - Centralized configuration management
- ✅ **UploadSession Tracking** - Monitor bulk upload progress
- ✅ **Enhanced Admin Panel** - Rich UI with statistics dashboard
- ✅ **Management Commands** - `addadmin`, `update_stats`
- ✅ **Audio Preview** - Inline player in admin interface
- ✅ **Color-coded Badges** - Format, status, and metrics indicators

### Version 2.0.0 (2026-01-30)

#### ✨ New Features
- ✅ Complete UI system with 4 design languages
- ✅ 108 KB of premium CSS components
- ✅ MSI Gaming, Spotify, Steam, Apple Glass themes

---

## 🚀 Roadmap

### v2.1.2 (Planned) - Smart Recommendations
- [ ] Listen history tracking
- [ ] Collaborative filtering
- [ ] Content-based recommendations
- [ ] Auto-generated playlists

### v2.2.0 (Future) - Audio Workshop
- [ ] Track mixing (dual player + crossfade)
- [ ] Basic waveform editor
- [ ] Trim, fade, normalize tools
- [ ] Mix export functionality

---

## 📚 Documentation

- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[COMPONENTS.md](COMPONENTS.md)** - UI components guide
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Deployment instructions

---

## 🔗 Links

- **Repository**: https://github.com/vitorpixel-6436/music-stream-app
- **Issues**: https://github.com/vitorpixel-6436/music-stream-app/issues
- **Releases**: https://github.com/vitorpixel-6436/music-stream-app/releases

---

## 👥 Author

**vitorpixel-6436**  
Email: vitorleitye6436@gmail.com

---

## 📜 License

MIT License - see LICENSE file for details

---

## 🔥 Support

Понравился проект? Поставь ⭐ на GitHub!

---

**Made with ❤️ using Django, Celery, yt-dlp & Vanilla JavaScript**  
**© 2026 Music Stream App. All rights reserved.**
