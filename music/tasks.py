"""Celery tasks for background processing"""

import logging
from pathlib import Path
from typing import Optional

from celery import shared_task
from django.conf import settings
from django.core.files import File
from django.utils import timezone

from .models import DownloadTask, MusicFile, Artist, Album, Genre
from .utils.downloader import MediaDownloader, DownloadProgressTracker

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def process_download_task(self, task_id: str):
    """
    Background task to download and process media from URL
    
    Args:
        task_id: UUID of DownloadTask
    
    Returns:
        dict: Result with status and track_id if successful
    """
    try:
        # Get task
        task = DownloadTask.objects.get(id=task_id)
        
        # Mark as started
        task.mark_started()
        
        # Initialize downloader
        downloader = MediaDownloader()
        
        # Step 1: Validate URL (5%)
        task.update_progress(5, "Validating URL...")
        is_valid, message = downloader.validate_url(task.url)
        
        if not is_valid:
            task.mark_failed(f"URL validation failed: {message}")
            return {'status': 'failed', 'error': message}
        
        # Step 2: Extract metadata (10%)
        task.update_progress(10, "Extracting video info...")
        video_info = downloader.get_video_info(task.url)
        
        if not video_info:
            task.mark_failed("Failed to extract video information")
            return {'status': 'failed', 'error': 'Info extraction failed'}
        
        # Update task with original metadata
        task.original_title = video_info.get('title', '')[:500]
        task.original_artist = video_info.get('artist', '')[:255]
        task.duration = video_info.get('duration', 0)
        task.save(update_fields=['original_title', 'original_artist', 'duration'])
        
        # Step 3: Download audio (10% -> 80%)
        task.update_progress(15, "Starting download...")
        
        # Create progress tracker
        def progress_callback(percent, step):
            # Map 0-100% download to 15-80% task progress
            task_percent = 15 + int(percent * 0.65)
            task.update_progress(task_percent, step)
        
        tracker = DownloadProgressTracker(task_id, progress_callback)
        
        downloaded_file = downloader.download_audio(
            url=task.url,
            output_format=task.output_format,
            quality=task.output_quality.replace('k', ''),
            progress_callback=tracker
        )
        
        if not downloaded_file or not downloaded_file.exists():
            task.mark_failed("Download completed but file not found")
            return {'status': 'failed', 'error': 'File not found'}
        
        # Step 4: Extract metadata from file (85%)
        task.update_progress(85, "Extracting metadata...")
        file_metadata = downloader.extract_metadata(downloaded_file)
        
        # Step 5: Create database entries (90%)
        task.update_progress(90, "Creating database entries...")
        
        # Get or create artist
        artist_name = task.original_artist or "Unknown Artist"
        artist, _ = Artist.objects.get_or_create(
            name=artist_name,
            defaults={'bio': ''}
        )
        
        # Create MusicFile
        track_title = task.original_title or downloaded_file.stem
        
        with open(downloaded_file, 'rb') as f:
            django_file = File(f, name=downloaded_file.name)
            
            track = MusicFile.objects.create(
                title=track_title,
                artist=artist,
                format=task.output_format,
                duration=file_metadata.get('duration', task.duration or 0),
                bitrate=file_metadata.get('bitrate', int(task.output_quality.replace('k', ''))),
                file_size=downloaded_file.stat().st_size,
            )
            
            # Move file to proper location
            track.file.save(downloaded_file.name, django_file, save=True)
        
        # Step 6: Cleanup (95%)
        task.update_progress(95, "Cleaning up...")
        downloader.cleanup_file(downloaded_file)
        
        # Step 7: Mark completed (100%)
        task.mark_completed(track)
        
        logger.info(f"Download task {task_id} completed successfully. Track ID: {track.id}")
        
        return {
            'status': 'completed',
            'track_id': str(track.id),
            'title': track.title,
        }
        
    except DownloadTask.DoesNotExist:
        logger.error(f"DownloadTask {task_id} not found")
        return {'status': 'failed', 'error': 'Task not found'}
    
    except Exception as e:
        logger.error(f"Download task {task_id} failed: {str(e)}", exc_info=True)
        
        try:
            task = DownloadTask.objects.get(id=task_id)
            
            # Retry logic
            if task.retry_count < 3:
                task.retry_count += 1
                task.save(update_fields=['retry_count'])
                
                # Retry with exponential backoff
                countdown = 60 * (2 ** task.retry_count)
                raise self.retry(exc=e, countdown=countdown)
            else:
                task.mark_failed(f"Max retries exceeded: {str(e)}")
        except Exception:
            pass
        
        return {'status': 'failed', 'error': str(e)}


@shared_task
def cleanup_old_failed_tasks():
    """
    Periodic task to cleanup old failed download tasks
    Runs daily to remove tasks older than 7 days
    """
    from datetime import timedelta
    
    cutoff_date = timezone.now() - timedelta(days=7)
    
    deleted_count = DownloadTask.objects.filter(
        status='failed',
        created_at__lt=cutoff_date
    ).delete()[0]
    
    logger.info(f"Cleaned up {deleted_count} old failed download tasks")
    
    return {'deleted': deleted_count}


@shared_task
def retry_failed_downloads():
    """
    Periodic task to retry failed downloads (up to 3 attempts)
    Runs every 6 hours
    """
    failed_tasks = DownloadTask.objects.filter(
        status='failed',
        retry_count__lt=3
    )[:10]  # Limit to 10 at a time
    
    retried_count = 0
    
    for task in failed_tasks:
        task.status = 'pending'
        task.progress = 0
        task.error_message = ''
        task.save(update_fields=['status', 'progress', 'error_message'])
        
        # Queue for processing
        process_download_task.delay(str(task.id))
        retried_count += 1
    
    logger.info(f"Retried {retried_count} failed download tasks")
    
    return {'retried': retried_count}
