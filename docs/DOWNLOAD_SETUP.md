# Download Manager Setup Guide

## 🚀 Quick Start

### 1. Install Dependencies

The download manager uses `yt-dlp` for downloading media from YouTube, SoundCloud, and Bandcamp.

```bash
pip install yt-dlp
```

**Note:** `yt-dlp` is already in `requirements.txt`, so if you installed dependencies, you're good to go!

### 2. Install FFmpeg

FFmpeg is required for audio conversion.

#### Windows
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

#### macOS
```bash
brew install ffmpeg
```

### 3. Verify Installation

```bash
ffmpeg -version
yt-dlp --version
```

---

## ⚙️ Configuration

### Settings

In your `settings.py`, ensure these directories exist:

```python
import os

BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Download temp directory (auto-created)
DOWNLOAD_TEMP_DIR = os.path.join(MEDIA_ROOT, 'temp', 'downloads')
```

### Optional: Concurrent Downloads

In `music/download_views.py`, adjust max concurrent downloads:

```python
# Default is 3
process_pending_downloads(max_concurrent=5)  # Increase to 5
```

---

## 🎯 Usage

### Creating a Download Task

#### Via Web Interface

1. Navigate to `/music/downloads/create/`
2. Paste YouTube/SoundCloud/Bandcamp URL
3. Select output format (mp3, flac, etc.)
4. Choose quality (320k recommended)
5. Click "Start Download"

#### Via API

```bash
curl -X POST http://localhost:8000/music/downloads/create/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "url=https://youtube.com/watch?v=dQw4w9WgXcQ&output_format=mp3&output_quality=320k"
```

### Monitoring Progress

#### Real-time Status

```javascript
// Poll for progress updates
setInterval(async () => {
  const response = await fetch(`/music/api/downloads/${taskId}/status/`);
  const data = await response.json();
  console.log(`Progress: ${data.progress}% - ${data.current_step}`);
}, 2000);
```

---

## 🧪 Testing

### Test URLs

These are safe test URLs you can use:

```
YouTube:
- https://www.youtube.com/watch?v=jNQXAC9IVRw (Me at the zoo)

SoundCloud:
- https://soundcloud.com/forss/flickermood

Bandcamp:
- https://freemusicarchive.bandcamp.com/track/lo-boob-oscillator
```

### Manual Testing

```python
from music.models import DownloadTask
from django.contrib.auth.models import User
from music.tasks import process_download_task_async

# Create test task
user = User.objects.first()
task = DownloadTask.objects.create(
    user=user,
    url='https://www.youtube.com/watch?v=jNQXAC9IVRw',
    output_format='mp3',
    output_quality='192k',
    source_type='youtube',
    status='pending'
)

# Start processing
process_download_task_async(str(task.id))

# Check status
task.refresh_from_db()
print(f"Status: {task.status}, Progress: {task.progress}%")
```

---

## 🐛 Troubleshooting

### Issue: "yt-dlp not installed"

**Solution:**
```bash
pip install --upgrade yt-dlp
```

### Issue: "FFmpeg not found"

**Solution:**
1. Install FFmpeg (see Installation section)
2. Ensure `ffmpeg` is in your PATH:
   ```bash
   ffmpeg -version
   ```

### Issue: Download fails with "HTTP Error 403"

**Solution:**
Update yt-dlp to latest version:
```bash
pip install --upgrade yt-dlp
```

YouTube frequently changes their API, and yt-dlp needs updates.

### Issue: Metadata extraction fails

**Solution:**
Ensure `mutagen` is installed:
```bash
pip install --upgrade mutagen
```

### Issue: Downloads are slow

**Possible causes:**
1. Network speed limitation
2. Source server throttling
3. Too many concurrent downloads

**Solutions:**
- Reduce concurrent downloads
- Use lower quality settings
- Check network connection

### Issue: Temp files not cleaned up

**Solution:**
Manually clean temp directory:
```bash
rm -rf media/temp/downloads/*
```

Or via Django shell:
```python
import os
import shutil
from django.conf import settings

temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp', 'downloads')
for file in os.listdir(temp_dir):
    file_path = os.path.join(temp_dir, file)
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Error removing {file}: {e}")
```

---

## 🔧 Advanced Configuration

### Custom Download Options

Edit `music/downloaders.py` to customize yt-dlp options:

```python
def _get_yt_dlp_options(self) -> Dict:
    options = {
        'format': 'bestaudio/best',
        # Add custom options here
        'socket_timeout': 60,  # Increase timeout
        'retries': 5,          # More retries
        'fragment_retries': 10,
        # Enable cookies for age-restricted videos
        'cookiefile': '/path/to/cookies.txt',
    }
    return options
```

### Periodic Queue Processing

Create a management command for cron:

```python
# music/management/commands/process_downloads.py
from django.core.management.base import BaseCommand
from music.tasks import process_pending_downloads

class Command(BaseCommand):
    help = 'Process pending download tasks'
    
    def handle(self, *args, **options):
        process_pending_downloads(max_concurrent=3)
        self.stdout.write('Download queue processed')
```

Add to crontab:
```bash
* * * * * cd /path/to/project && python manage.py process_downloads
```

---

## 📊 Monitoring

### Check Active Downloads

```python
from music.tasks import get_active_task_count

active_count = get_active_task_count()
print(f"Active downloads: {active_count}")
```

### Download Statistics

```python
from music.models import DownloadTask
from django.db.models import Count

stats = DownloadTask.objects.values('status').annotate(
    count=Count('id')
)

for stat in stats:
    print(f"{stat['status']}: {stat['count']} tasks")
```

---

## 🚀 Migration to Celery (Optional)

For production environments with high load, consider migrating to Celery.

See commented code in `music/tasks.py` for Celery integration examples.

---

## 📝 Support

For issues or questions:
1. Check [DOWNLOAD_API.md](DOWNLOAD_API.md) for API documentation
2. Review logs in `logs/` directory
3. Open an issue on GitHub

---

## ✅ Checklist

- [ ] yt-dlp installed and updated
- [ ] FFmpeg installed and in PATH
- [ ] Media directories configured
- [ ] Test download successful
- [ ] Progress tracking working
- [ ] Cleanup on completion verified
