"""
Background Tasks for Music Download
====================================

Celery/Django-Q tasks for downloading media from YouTube, SoundCloud, etc.
using yt-dlp with progress tracking and error handling.

Requirements:
    pip install yt-dlp celery django-celery-results
"""

import os
import logging
import tempfile
from pathlib import Path
from typing import Optional

from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.utils import timezone

try:
    from celery import shared_task
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False
    # Fallback decorator for non-Celery environments
    def shared_task(func):
        return func

try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False
    logging.warning("yt-dlp not installed. Install with: pip install yt-dlp")

from mutagen import File as MutagenFile
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB

from .models import DownloadTask, MusicFile, Artist, Album

logger = logging.getLogger(__name__)


class DownloadProgressHook:
    """Progress hook for yt-dlp to update task progress"""
    
    def __init__(self, task_id):
        self.task_id = task_id
        self.task = None
    
    def __call__(self, d):
        """Called by yt-dlp with download progress info"""
        if not self.task:
            try:
                self.task = DownloadTask.objects.get(id=self.task_id)
            except DownloadTask.DoesNotExist:
                return
        
        if d['status'] == 'downloading':
            # Calculate progress percentage
            if 'total_bytes' in d and d['total_bytes']:
                progress = int((d['downloaded_bytes'] / d['total_bytes']) * 70)  # 0-70%
            elif '_percent_str' in d:
                # Fallback to percent string parsing
                percent_str = d['_percent_str'].strip('%')
                try:
                    progress = int(float(percent_str) * 0.7)
                except:
                    progress = 0
            else:
                progress = 0
            
            self.task.update_progress(progress, f"Downloading: {d.get('_percent_str', '...')}")
        
        elif d['status'] == 'finished':
            self.task.update_progress(70, "Download complete, processing...")


@shared_task(bind=True, max_retries=3)
def process_download_task(self, task_id: str):
    """
    Process a download task: download media, extract metadata, create MusicFile.
    
    Args:
        task_id: UUID of DownloadTask
    
    Returns:
        dict: Result with status and track_id if successful
    """
    if not YT_DLP_AVAILABLE:
        logger.error("yt-dlp not available")
        return {'status': 'error', 'message': 'yt-dlp not installed'}
    
    try:
        task = DownloadTask.objects.get(id=task_id)
    except DownloadTask.DoesNotExist:
        logger.error(f"DownloadTask {task_id} not found")
        return {'status': 'error', 'message': 'Task not found'}
    
    try:
        # Mark task as started
        task.mark_started()
        logger.info(f"Starting download: {task.url}")
        
        # Create temp directory
        temp_dir = Path(tempfile.mkdtemp(prefix='music_download_'))
        output_path = temp_dir / 'downloaded_audio'
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(output_path),
            'progress_hooks': [DownloadProgressHook(task_id)],
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'writethumbnail': True,  # Download thumbnail for cover art
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': task.output_format,
                'preferredquality': task.output_quality.replace('k', ''),
            }],
            # Metadata
            'add_metadata': True,
            'embed_thumbnail': True,
        }
        
        # Download with yt-dlp
        task.update_progress(5, "Fetching metadata...")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info first
            info = ydl.extract_info(task.url, download=False)
            
            # Save metadata to task
            task.original_title = info.get('title', '')
            task.original_artist = info.get('uploader', '') or info.get('channel', '')
            task.duration = info.get('duration')
            task.save(update_fields=['original_title', 'original_artist', 'duration'])
            
            # Download
            task.update_progress(10, "Downloading audio...")
            ydl.download([task.url])
        
        # Find downloaded file (yt-dlp adds extension)
        downloaded_file = None
        for ext in [task.output_format, 'mp3', 'm4a', 'opus']:
            potential_file = output_path.with_suffix(f'.{ext}')
            if potential_file.exists():
                downloaded_file = potential_file
                break
        
        if not downloaded_file or not downloaded_file.exists():
            raise FileNotFoundError("Downloaded file not found")
        
        task.update_progress(75, "Extracting metadata...")
        
        # Extract metadata with mutagen
        audio = MutagenFile(str(downloaded_file), easy=True)
        metadata = {}
        if audio:
            metadata = {
                'title': audio.get('title', [task.original_title])[0],
                'artist': audio.get('artist', [task.original_artist])[0],
                'album': audio.get('album', [''])[0],
            }
        else:
            metadata = {
                'title': task.original_title,
                'artist': task.original_artist,
                'album': '',
            }
        
        # Create or get artist
        artist, _ = Artist.objects.get_or_create(
            name=metadata['artist'] or 'Unknown Artist'
        )
        
        # Create album if specified
        album = None
        if metadata.get('album'):
            album, _ = Album.objects.get_or_create(
                title=metadata['album'],
                artist=artist
            )
        
        task.update_progress(85, "Creating music file...")
        
        # Create MusicFile
        with open(downloaded_file, 'rb') as f:
            music_file = MusicFile.objects.create(
                title=metadata['title'] or 'Unknown Title',
                artist=artist,
                album=album,
                format=task.output_format,
            )
            music_file.file.save(
                f"{metadata['title']}.{task.output_format}",
                File(f),
                save=True
            )
        
        # Try to add cover art from thumbnail
        task.update_progress(90, "Adding cover art...")
        thumbnail_paths = [
            output_path.with_suffix('.jpg'),
            output_path.with_suffix('.png'),
            output_path.with_suffix('.webp'),
        ]
        
        for thumb_path in thumbnail_paths:
            if thumb_path.exists():
                try:
                    with open(thumb_path, 'rb') as thumb_f:
                        music_file.cover_image.save(
                            f"cover_{music_file.id}.jpg",
                            File(thumb_f),
                            save=True
                        )
                    break
                except Exception as e:
                    logger.warning(f"Failed to save thumbnail: {e}")
        
        # Clean up temp files
        try:
            for file in temp_dir.iterdir():
                file.unlink()
            temp_dir.rmdir()
        except Exception as e:
            logger.warning(f"Cleanup failed: {e}")
        
        # Mark task as completed
        task.mark_completed(music_file)
        task.update_progress(100, "Complete!")
        
        logger.info(f"Download completed: {music_file.title} (ID: {music_file.id})")
        
        return {
            'status': 'success',
            'track_id': str(music_file.id),
            'title': music_file.title,
            'artist': artist.name,
        }
    
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Download task failed: {error_msg}", exc_info=True)
        
        # Retry logic
        if task.retry_count < 2:
            task.retry_count += 1
            task.save(update_fields=['retry_count'])
            raise self.retry(exc=e, countdown=60 * (task.retry_count + 1))
        else:
            task.mark_failed(error_msg)
        
        return {'status': 'error', 'message': error_msg}


@shared_task
def cleanup_old_failed_tasks():
    """
    Cleanup old failed download tasks (older than 30 days).
    Run this periodically via Celery Beat.
    """
    from datetime import timedelta
    
    cutoff_date = timezone.now() - timedelta(days=30)
    
    deleted = DownloadTask.objects.filter(
        status__in=['failed', 'cancelled'],
        created_at__lt=cutoff_date
    ).delete()
    
    logger.info(f"Cleaned up {deleted[0]} old download tasks")
    return deleted[0]


@shared_task
def retry_failed_tasks():
    """
    Retry failed tasks that haven't exceeded retry limit.
    """
    failed_tasks = DownloadTask.objects.filter(
        status='failed',
        retry_count__lt=3
    )[:10]  # Limit to 10 at a time
    
    retry_count = 0
    for task in failed_tasks:
        task.status = 'pending'
        task.error_message = ''
        task.save(update_fields=['status', 'error_message'])
        
        # Queue for processing
        process_download_task.delay(str(task.id))
        retry_count += 1
    
    logger.info(f"Queued {retry_count} failed tasks for retry")
    return retry_count
