# 🚀 Download Manager - Quick Start (5 Minutes)

## What You Get

✅ Download music from **YouTube, SoundCloud, Bandcamp**  
✅ **Real-time progress** tracking with live updates  
✅ **Automatic metadata** extraction (title, artist, album)  
✅ **Multiple formats**: MP3, FLAC, OGG, M4A, WAV  
✅ **Background processing** - no blocking  
✅ **Auto-retry** on failure (up to 3 attempts)  
✅ **Beautiful UI** with Steam-inspired design  

---

## Step 1: Install FFmpeg (One-Time)

### Windows
```bash
# Option 1: Chocolatey (recommended)
choco install ffmpeg

# Option 2: Scoop
scoop install ffmpeg

# Option 3: Manual
# Download from https://ffmpeg.org/download.html
# Extract and add to PATH
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update && sudo apt install -y ffmpeg
```

### macOS
```bash
brew install ffmpeg
```

### Verify
```bash
ffmpeg -version
# Should show FFmpeg version info
```

---

## Step 2: Install Python Dependencies

```bash
# Already included if you ran pip install -r requirements.txt
pip install yt-dlp mutagen
```

---

## Step 3: Your First Download

### Via Web Interface

1. Start Django server:
   ```bash
   python manage.py runserver
   ```

2. Open browser: `http://localhost:8000/music/downloads/create/`

3. Paste a YouTube URL (example):
   ```
   https://www.youtube.com/watch?v=jNQXAC9IVRw
   ```

4. Select:
   - **Format**: MP3
   - **Quality**: 320 kbps

5. Click **"Start Download"**

6. Watch real-time progress! 🎉

### Via Python Code

```python
from music.models import DownloadTask
from django.contrib.auth.models import User

# Get user
user = User.objects.first()  # or specific user

# Create download task
task = DownloadTask.objects.create(
    user=user,
    url='https://www.youtube.com/watch?v=jNQXAC9IVRw',
    output_format='mp3',
    output_quality='320k',
    source_type='youtube',
    status='pending'
)

# Processing starts automatically!
print(f"Task created: {task.id}")
print(f"Status: {task.status}")

# Check progress
task.refresh_from_db()
print(f"Progress: {task.progress}%")
```

---

## Step 4: Monitor Downloads

### Web Interface

Go to: `http://localhost:8000/music/downloads/`

You'll see:
- 📊 **Statistics** (Total, Active, Completed, Failed)
- 🔍 **Search & Filters** (by status, source)
- 📈 **Live Progress Bars** (updates every 2 seconds)
- ⏯️ **Actions** (Cancel, Retry, Play)

### API Endpoint

```bash
# Check single task status
curl http://localhost:8000/music/api/downloads/<TASK_ID>/status/

# Response:
{
  "success": true,
  "status": "downloading",
  "progress": 45,
  "current_step": "Downloading... 5.2MB/11.5MB (456KB/s)",
  "is_active": true
}
```

---

## Features Walkthrough

### 1. Multiple Formats

Supported output formats:
- **MP3**: Universal compatibility, good compression
- **FLAC**: Lossless, audiophile quality
- **OGG**: Open-source, good for streaming
- **M4A**: Apple devices, AAC codec
- **WAV**: Uncompressed, editing-ready

### 2. Quality Options

- **320 kbps**: Best quality (recommended)
- **256 kbps**: High quality
- **192 kbps**: Good quality, smaller size
- **128 kbps**: Acceptable quality, smallest size

### 3. Auto-Retry

If download fails (network issues, video removed, etc.):
- System automatically retries **up to 3 times**
- Exponential backoff between retries
- Manual retry button available

### 4. Metadata Extraction

Automatically extracted and saved:
- 🎵 **Title** from video title
- 🎤 **Artist** from uploader/channel
- 💿 **Album** if available
- ⏱️ **Duration** in seconds
- 📊 **Bitrate** after conversion
- 🖼️ **Cover art** (embedded in MP3/M4A)

### 5. Background Processing

- Downloads run in **background threads**
- No page blocking or freezing
- Up to **3 concurrent downloads**
- Automatic queue management

---

## Common Issues & Quick Fixes

### ❌ "FFmpeg not found"

**Fix:**
```bash
# Verify installation
ffmpeg -version

# If not found, install (see Step 1)
# Windows: Add to PATH if manually installed
```

### ❌ "HTTP Error 403" or "Video unavailable"

**Fix:**
```bash
# Update yt-dlp (YouTube changes API frequently)
pip install --upgrade yt-dlp
```

### ❌ Download stuck at 0%

**Reasons:**
- Server not running background tasks
- Task queue full (max 3 concurrent)

**Fix:**
```bash
# Check if task processing is running
# Visit /music/downloads/ - it auto-processes pending tasks

# Or manually in Django shell:
from music.tasks import process_pending_downloads
process_pending_downloads(max_concurrent=3)
```

### ❌ "Age-restricted video"

**Fix:**
Some videos require authentication. For now, use non-restricted videos.

---

## Test URLs (Safe & Free)

```
# YouTube
https://www.youtube.com/watch?v=jNQXAC9IVRw
  → "Me at the zoo" (First YouTube video)

# SoundCloud
https://soundcloud.com/forss/flickermood
  → Creative Commons music

# Bandcamp
https://freemusicarchive.bandcamp.com/track/lo-boob-oscillator
  → Free Music Archive
```

---

## Performance Tips

### For Faster Downloads

1. **Use lower quality** for testing (128k or 192k)
2. **Limit concurrent downloads** to 2-3
3. **Stable internet** connection

### For Better Quality

1. **320 kbps MP3** for best balance
2. **FLAC format** for lossless audio
3. **Check source quality** (some videos have low-quality audio)

---

## What's Next?

### Immediate
- ✅ Download your first track
- ✅ Try different formats
- ✅ Test with SoundCloud/Bandcamp

### Advanced
- 🔧 Migrate to Celery for production (see `music/tasks.py`)
- 📦 Set up periodic queue processing (cron job)
- 📊 Add usage analytics
- 🔒 Implement rate limiting per user

---

## Documentation Links

- **API Reference**: [DOWNLOAD_API.md](DOWNLOAD_API.md)
- **Full Setup Guide**: [DOWNLOAD_SETUP.md](DOWNLOAD_SETUP.md)
- **Architecture**: Backend docs coming soon

---

## Quick Reference

```bash
# Check FFmpeg
ffmpeg -version

# Update yt-dlp
pip install --upgrade yt-dlp

# Start server
python manage.py runserver

# Access download manager
http://localhost:8000/music/downloads/

# Create new download
http://localhost:8000/music/downloads/create/
```

---

## 🎉 Success!

You're ready to download music! If you encounter issues:

1. Check [DOWNLOAD_SETUP.md](DOWNLOAD_SETUP.md) for detailed troubleshooting
2. Review logs in Django console
3. Open an issue on GitHub

**Happy downloading!** 🎵
