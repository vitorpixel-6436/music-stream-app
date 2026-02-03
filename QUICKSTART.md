# ⚡ Quick Start Guide - Music Stream App

**Get up and running in 5 minutes!**

---

## 👀 TL;DR

```bash
# Linux/macOS
git clone https://github.com/vitorpixel-6436/music-stream-app.git
cd music-stream-app
chmod +x install.sh && ./install.sh
source venv/bin/activate
python manage.py runserver

# Windows
git clone https://github.com/vitorpixel-6436/music-stream-app.git
cd music-stream-app
install.bat
venv\Scripts\activate
python manage.py runserver
```

**Visit:** http://localhost:8000

---

## 💻 Step-by-Step

### 🐧 Linux / 🍎 macOS

**1. Clone the repository:**
```bash
git clone https://github.com/vitorpixel-6436/music-stream-app.git
cd music-stream-app
```

**2. Run the automatic installer:**
```bash
chmod +x install.sh
./install.sh
```

The installer will:
- ✅ Check Python 3.10+ is installed
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Setup database and run migrations
- ✅ Create admin user (you'll be prompted)
- ✅ Collect static files
- ✅ Setup recommendation engine

**3. Start the server:**
```bash
source venv/bin/activate
python manage.py runserver
```

**4. Open your browser:**
```
http://localhost:8000
```

---

### 💻 Windows

**1. Clone the repository:**
```cmd
git clone https://github.com/vitorpixel-6436/music-stream-app.git
cd music-stream-app
```

**2. Run the automatic installer:**

Double-click `install.bat` or run in Command Prompt:
```cmd
install.bat
```

The installer will:
- ✅ Check Python 3.10+ is installed
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Setup database and run migrations
- ✅ Create admin user (you'll be prompted)
- ✅ Collect static files
- ✅ Setup recommendation engine

**3. Start the server:**
```cmd
venv\Scripts\activate
python manage.py runserver
```

**4. Open your browser:**
```
http://localhost:8000
```

---

## 🌐 Access Points

After starting the server:

| **Feature** | **URL** |
|-------------|----------|
| Main App | http://localhost:8000 |
| Download Manager | http://localhost:8000/music/downloads/ |
| Admin Panel | http://localhost:8000/admin/ |
| Recommendations API | http://localhost:8000/music/api/recommendations/ |
| Top Charts | http://localhost:8000/music/api/charts/ |

---

## 🎵 What's Next?

### Upload Your First Track

1. Go to http://localhost:8000/admin/
2. Login with your superuser account
3. Click "Music files" → "Add music file"
4. Upload an MP3/FLAC file
5. It's now available in the main app!

### Try the Download Manager

1. **Install FFmpeg** (required):
   - **Windows:** `choco install ffmpeg`
   - **Linux:** `sudo apt install ffmpeg`
   - **macOS:** `brew install ffmpeg`

2. Go to http://localhost:8000/music/downloads/create/
3. Paste a YouTube/SoundCloud URL
4. Click "Start Download"
5. Watch real-time progress!

### Explore Recommendations

1. Listen to some tracks
2. Visit http://localhost:8000/music/api/recommendations/
3. Get personalized recommendations based on your listening history!

---

## ⚠️ Common Issues

### "Python not found"

**Problem:** Python is not installed or not in PATH.

**Solution:**
- Download Python 3.10+ from https://python.org/downloads/
- During installation, check "Add Python to PATH"

### "Permission denied: install.sh"

**Problem:** Script is not executable (Linux/macOS).

**Solution:**
```bash
chmod +x install.sh
```

### "FFmpeg not found"

**Problem:** FFmpeg is not installed (needed for Download Manager).

**Solution:**
- **Windows:** `choco install ffmpeg` (requires Chocolatey)
- **Linux:** `sudo apt install ffmpeg`
- **macOS:** `brew install ffmpeg`
- **Manual:** Download from https://ffmpeg.org/download.html

### "Cannot import name 'RecommendationEngine'"

**Problem:** Database migrations not applied.

**Solution:**
```bash
python manage.py migrate
```

### Static files not loading

**Problem:** Static files not collected.

**Solution:**
```bash
python manage.py collectstatic
```

---

## 📚 Full Documentation

For detailed information, see:

- 📖 [**README.md**](README.md) - Full project overview
- 🔧 [**INSTALL.md**](INSTALL.md) - Detailed installation guide
- 🤖 [**Recommendation Engine**](docs/RECOMMENDATIONS.md) - ML algorithms & API
- 📥 [**Download Manager**](docs/DOWNLOAD_QUICKSTART.md) - 5-minute download guide
- 🎨 [**Steam UI**](steam_ui/README.md) - UI component library

---

## 🚀 Pro Tips

### Enable Redis Caching (Optional)

For faster recommendations:

```bash
# Install Redis
sudo apt install redis-server  # Linux
brew install redis            # macOS

# Start Redis
redis-server

# Add to .env
REDIS_URL=redis://127.0.0.1:6379/1
```

### Production Deployment

See full deployment guide in [README.md](README.md#-deployment)

### Development Mode

```bash
# Enable debug mode (already enabled by installer)
DEBUG=True  # in .env

# Run with auto-reload
python manage.py runserver
```

---

## ❓ Need Help?

- 🐛 [**Report Issues**](https://github.com/vitorpixel-6436/music-stream-app/issues)
- 📚 [**Full Documentation**](README.md)
- 💬 [**Discussions**](https://github.com/vitorpixel-6436/music-stream-app/discussions)

---

**Happy streaming! 🎵**

*Made with ❤️ by vitorpixel-6436*
