# 🚀 Quick Fix: Download Manager Setup

## 🐛 Problem
You're getting 404 on `/music/downloads/create/` because some setup steps are missing.

## ✅ Solution (5 Minutes)

### Step 1: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Create Anonymous User (for testing)

```bash
python manage.py shell
```

Then in the shell:
```python
from django.contrib.auth.models import User
User.objects.get_or_create(
    username='anonymous',
    defaults={'email': 'anonymous@test.com'}
)
exit()
```

### Step 3: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 4: Restart Server

```bash
python manage.py runserver
```

### Step 5: Test It!

Open browser: `http://localhost:8000/music/downloads/create/`

You should see the download form! 🎉

---

## 📦 Install FFmpeg (Required)

### Windows
```bash
choco install ffmpeg
```

### Linux
```bash
sudo apt install ffmpeg
```

### macOS
```bash
brew install ffmpeg
```

### Verify
```bash
ffmpeg -version
```

---

## 🧪 Test Download

1. Go to: `http://localhost:8000/music/downloads/create/`
2. Paste URL: `https://www.youtube.com/watch?v=jNQXAC9IVRw`
3. Select: MP3 + 320k
4. Click "Start Download"
5. Watch progress at: `http://localhost:8000/music/downloads/`

---

## 🐛 Common Issues

### Issue: "yt-dlp not installed"

**Fix:**
```bash
pip install yt-dlp mutagen
```

### Issue: "FFmpeg not found"

**Fix:**
Install FFmpeg (see above), then verify:
```bash
ffmpeg -version
```

### Issue: "No module named 'steam_ui'"

**Fix:**
steam_ui should be in the project. If missing:
```bash
# Check if folder exists
ls steam_ui/

# If missing, it's in the repo - pull latest
git pull origin main
```

### Issue: Static files 404

**Fix:**
```bash
python manage.py collectstatic --noinput
```

### Issue: "Page not found (404)"

**Fix:**
Check that you pulled the latest code:
```bash
git pull origin main
python manage.py migrate
python manage.py runserver
```

---

## 📝 Full Setup Checklist

- [ ] `git pull origin main`
- [ ] `pip install -r requirements.txt`
- [ ] `pip install yt-dlp mutagen`
- [ ] Install FFmpeg
- [ ] `python manage.py makemigrations`
- [ ] `python manage.py migrate`
- [ ] `python manage.py collectstatic --noinput`
- [ ] Create anonymous user (see Step 2)
- [ ] `python manage.py runserver`
- [ ] Test: `http://localhost:8000/music/downloads/create/`

---

## 🎉 Success!

If you see the download form, you're ready to go!

Next steps:
- Try downloading a YouTube video
- Check progress in real-time
- View your downloads at `/music/downloads/`

---

## 📚 Full Documentation

- [Quick Start (5 min)](docs/DOWNLOAD_QUICKSTART.md)
- [Full Setup Guide](docs/DOWNLOAD_SETUP.md)
- [API Reference](docs/DOWNLOAD_API.md)
