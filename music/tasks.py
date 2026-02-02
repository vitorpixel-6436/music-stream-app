"""
Background Task Processing
===========================

Background task processor for download tasks.
Currently using threading for simplicity.

Features:
- Asynchronous task processing
- Automatic retries on failure
- Progress tracking
- Error logging
- Thread-safe queue management

Migration Path:
- Can be easily migrated to Celery or Django-Q
- Just replace process_download_task() decorator
"""

import logging
import threading
import traceback
from django.utils import timezone
from .models import DownloadTask
from .downloaders import get_downloader, create_music_file_from_download, DownloadError

logger = logging.getLogger(__name__)

# Thread-safe queue for pending tasks
active_threads = {}
thread_lock = threading.Lock()


def process_download_task(task_id: str):
    """
    Process a download task in background.
    
    This function:
    1. Downloads media using appropriate downloader
    2. Extracts metadata
    3. Creates MusicFile object
    4. Updates task status
    5. Handles errors and retries
    
    Args:
        task_id: UUID of DownloadTask to process
    """
    try:
        task = DownloadTask.objects.get(id=task_id)
    except DownloadTask.DoesNotExist:
        logger.error(f"Task {task_id} not found")
        return
    
    # Mark as started
    task.mark_started()
    logger.info(f"Processing download task: {task.id}")
    
    downloaded_file = None
    
    try:
        # Get appropriate downloader
        downloader = get_downloader(task)
        
        # Download media
        task.update_progress(10, "Starting download...")
        downloaded_file = downloader.download()
        
        # Extract metadata
        task.update_progress(90, "Extracting metadata...")
        metadata = downloader.extract_metadata(downloaded_file)
        
        # Create MusicFile
        task.update_progress(95, "Creating music file...")
        music_file = create_music_file_from_download(task, downloaded_file, metadata)
        
        # Mark as completed
        task.mark_completed(music_file)
        task.update_progress(100, "Complete!")
        
        logger.info(
            f"Download task {task.id} completed successfully. "
            f"Created MusicFile: {music_file.id}"
        )
        
        # Cleanup temp file
        if downloaded_file:
            downloader.cleanup(downloaded_file)
    
    except DownloadError as e:
        # Known download error
        error_msg = str(e)
        logger.error(f"Download task {task.id} failed: {error_msg}")
        
        # Check if should retry
        if task.retry_count < 3:
            task.retry_count += 1
            task.status = 'pending'
            task.error_message = f"Retry {task.retry_count}/3: {error_msg}"
            task.save(update_fields=['retry_count', 'status', 'error_message'])
            
            logger.info(f"Retrying task {task.id} (attempt {task.retry_count})")
            # Will be picked up by queue manager
        else:
            task.mark_failed(error_msg)
    
    except Exception as e:
        # Unexpected error
        error_msg = f"Unexpected error: {str(e)}"
        error_trace = traceback.format_exc()
        
        logger.error(
            f"Download task {task.id} failed with unexpected error:\n{error_trace}"
        )
        
        task.mark_failed(error_msg)
    
    finally:
        # Remove from active threads
        with thread_lock:
            if task_id in active_threads:
                del active_threads[task_id]


def process_download_task_async(task_id: str):
    """
    Start processing download task in background thread.
    
    Args:
        task_id: UUID string of DownloadTask
    
    Returns:
        threading.Thread object
    """
    task_id_str = str(task_id)
    
    with thread_lock:
        # Check if already processing
        if task_id_str in active_threads:
            logger.warning(f"Task {task_id_str} is already being processed")
            return active_threads[task_id_str]
        
        # Create and start thread
        thread = threading.Thread(
            target=process_download_task,
            args=(task_id_str,),
            name=f"DownloadTask-{task_id_str[:8]}",
            daemon=True
        )
        
        active_threads[task_id_str] = thread
        thread.start()
        
        logger.info(f"Started background thread for task {task_id_str}")
        return thread


def get_active_task_count() -> int:
    """
    Get number of currently processing tasks.
    
    Returns:
        Number of active threads
    """
    with thread_lock:
        # Clean up finished threads
        finished = [tid for tid, thread in active_threads.items() if not thread.is_alive()]
        for tid in finished:
            del active_threads[tid]
        
        return len(active_threads)


def cancel_task_processing(task_id: str) -> bool:
    """
    Attempt to cancel a running task.
    Note: This only removes from queue, actual thread cancellation is not guaranteed.
    
    Args:
        task_id: UUID string of task to cancel
    
    Returns:
        True if task was in queue and removed
    """
    task_id_str = str(task_id)
    
    with thread_lock:
        if task_id_str in active_threads:
            # Note: We can't force-kill threads in Python
            # Just mark task as cancelled in DB and remove from tracking
            logger.warning(
                f"Task {task_id_str} is being processed, "
                f"cancellation may not be immediate"
            )
            del active_threads[task_id_str]
            return True
        return False


# ============================================================================
# Queue Manager - Processes pending tasks
# ============================================================================

def process_pending_downloads(max_concurrent: int = 3):
    """
    Process pending download tasks up to max_concurrent limit.
    
    This can be called:
    - By a management command (periodic)
    - After creating a new task
    - By a cron job
    
    Args:
        max_concurrent: Maximum number of concurrent downloads
    """
    current_active = get_active_task_count()
    
    if current_active >= max_concurrent:
        logger.debug(
            f"Max concurrent downloads reached ({current_active}/{max_concurrent})"
        )
        return
    
    # Get pending tasks
    slots_available = max_concurrent - current_active
    pending_tasks = DownloadTask.objects.filter(
        status='pending'
    ).order_by('created_at')[:slots_available]
    
    for task in pending_tasks:
        logger.info(f"Starting pending task: {task.id}")
        process_download_task_async(str(task.id))


# ============================================================================
# Celery/Django-Q Migration Helpers
# ============================================================================

# Uncomment when migrating to Celery:
# from celery import shared_task
#
# @shared_task(bind=True, max_retries=3)
# def process_download_task_celery(self, task_id: str):
#     """Celery version of process_download_task"""
#     try:
#         process_download_task(task_id)
#     except Exception as exc:
#         raise self.retry(exc=exc, countdown=60)

# Uncomment when migrating to Django-Q:
# from django_q.tasks import async_task
#
# def process_download_task_djangoq(task_id: str):
#     """Django-Q version"""
#     async_task(
#         'music.tasks.process_download_task',
#         task_id,
#         hook='music.tasks.download_complete_hook'
#     )
