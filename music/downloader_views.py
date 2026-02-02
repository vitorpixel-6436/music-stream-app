"""
Downloader Views
================

Views for YouTube/SoundCloud downloader functionality.
"""

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.html import escape

from .models import DownloadTask
from .forms import URLImportForm

try:
    from .tasks import process_download_task
    TASKS_AVAILABLE = True
except ImportError:
    TASKS_AVAILABLE = False
    logging.warning("Celery tasks not available")

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["GET", "POST"])
def create_download(request):
    """
    Create a new download task from URL.
    Supports YouTube, SoundCloud, Bandcamp, and direct URLs.
    """
    if request.method == 'POST':
        form = URLImportForm(request.POST)
        
        if form.is_valid():
            try:
                # Create download task
                task = DownloadTask.objects.create(
                    user=request.user,
                    url=form.cleaned_data['url'],
                    source_type=form.cleaned_data.get('source_type', 'youtube'),
                    output_format=form.cleaned_data.get('output_format', 'mp3'),
                    output_quality=form.cleaned_data.get('output_quality', '320k'),
                )
                
                # Queue background task
                if TASKS_AVAILABLE:
                    process_download_task.delay(str(task.id))
                    messages.success(
                        request,
                        f'✅ Download task created! Track ID: {str(task.id)[:8]}'
                    )
                else:
                    messages.warning(
                        request,
                        'Background tasks not configured. Download queued for manual processing.'
                    )
                
                # Redirect based on request type
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'task_id': str(task.id),
                        'message': 'Download started'
                    })
                
                return redirect('music:download_manager')
            
            except Exception as e:
                logger.error(f"Download creation error: {e}", exc_info=True)
                messages.error(request, f'Error creating download: {str(e)}')
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'error',
                        'message': str(e)
                    }, status=400)
        else:
            # Form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'errors': form.errors
                }, status=400)
    else:
        form = URLImportForm()
    
    return render(request, 'music/download_create.html', {'form': form})


@login_required
def download_manager(request):
    """
    Display user's download tasks with filtering and pagination.
    """
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('q', '').strip()
    
    # Base queryset
    tasks = DownloadTask.objects.filter(user=request.user)
    
    # Apply filters
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    
    if search_query:
        safe_query = escape(search_query)
        tasks = tasks.filter(
            Q(original_title__icontains=safe_query) |
            Q(original_artist__icontains=safe_query) |
            Q(url__icontains=safe_query)
        )
    
    # Order by creation date
    tasks = tasks.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(tasks, 20)
    page = request.GET.get('page', 1)
    tasks_page = paginator.get_page(page)
    
    # Statistics
    stats = {
        'total': DownloadTask.objects.filter(user=request.user).count(),
        'pending': DownloadTask.objects.filter(user=request.user, status='pending').count(),
        'downloading': DownloadTask.objects.filter(user=request.user, status='downloading').count(),
        'completed': DownloadTask.objects.filter(user=request.user, status='completed').count(),
        'failed': DownloadTask.objects.filter(user=request.user, status='failed').count(),
    }
    
    context = {
        'tasks': tasks_page,
        'stats': stats,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': DownloadTask.STATUS_CHOICES,
    }
    
    return render(request, 'music/download_manager.html', context)


@login_required
@require_http_methods(["GET"])
def download_progress(request, task_id):
    """
    API endpoint to get real-time progress of a download task.
    Used for AJAX polling.
    """
    try:
        task = get_object_or_404(
            DownloadTask,
            id=task_id,
            user=request.user
        )
        
        return JsonResponse({
            'status': task.status,
            'progress': task.progress,
            'current_step': task.current_step,
            'original_title': task.original_title,
            'original_artist': task.original_artist,
            'error_message': task.error_message,
            'is_active': task.is_active,
            'result_track_id': str(task.result_track.id) if task.result_track else None,
        })
    
    except Exception as e:
        logger.error(f"Progress check error: {e}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@login_required
@require_POST
def cancel_download(request, task_id):
    """
    Cancel a pending or active download task.
    """
    try:
        task = get_object_or_404(
            DownloadTask,
            id=task_id,
            user=request.user
        )
        
        if task.is_active:
            task.status = 'cancelled'
            task.save(update_fields=['status'])
            
            messages.success(request, 'Download cancelled')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Cancelled'})
        else:
            messages.warning(request, 'Task is not active')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Not active'}, status=400)
    
    except Exception as e:
        logger.error(f"Cancel error: {e}")
        messages.error(request, 'Failed to cancel download')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return redirect('music:download_manager')


@login_required
@require_POST
def retry_download(request, task_id):
    """
    Retry a failed download task.
    """
    try:
        task = get_object_or_404(
            DownloadTask,
            id=task_id,
            user=request.user
        )
        
        if task.status == 'failed':
            # Reset task
            task.status = 'pending'
            task.progress = 0
            task.current_step = ''
            task.error_message = ''
            task.retry_count += 1
            task.save(update_fields=['status', 'progress', 'current_step', 'error_message', 'retry_count'])
            
            # Re-queue task
            if TASKS_AVAILABLE:
                process_download_task.delay(str(task.id))
                messages.success(request, 'Download retry queued')
            else:
                messages.warning(request, 'Background tasks not configured')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Retrying'})
        else:
            messages.warning(request, 'Only failed tasks can be retried')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Not failed'}, status=400)
    
    except Exception as e:
        logger.error(f"Retry error: {e}")
        messages.error(request, 'Failed to retry download')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return redirect('music:download_manager')


@login_required
@require_POST
def delete_download(request, task_id):
    """
    Delete a download task (does not delete the resulting track).
    """
    try:
        task = get_object_or_404(
            DownloadTask,
            id=task_id,
            user=request.user
        )
        
        task.delete()
        messages.success(request, 'Download task deleted')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Deleted'})
    
    except Exception as e:
        logger.error(f"Delete error: {e}")
        messages.error(request, 'Failed to delete task')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return redirect('music:download_manager')


@login_required
def download_stats(request):
    """
    API endpoint for download statistics.
    """
    stats = {
        'total': DownloadTask.objects.filter(user=request.user).count(),
        'pending': DownloadTask.objects.filter(user=request.user, status='pending').count(),
        'downloading': DownloadTask.objects.filter(user=request.user, status='downloading').count(),
        'processing': DownloadTask.objects.filter(user=request.user, status='processing').count(),
        'completed': DownloadTask.objects.filter(user=request.user, status='completed').count(),
        'failed': DownloadTask.objects.filter(user=request.user, status='failed').count(),
        'cancelled': DownloadTask.objects.filter(user=request.user, status='cancelled').count(),
    }
    
    # Recent activity (last 24 hours)
    from datetime import timedelta
    from django.utils import timezone
    
    recent_cutoff = timezone.now() - timedelta(hours=24)
    stats['recent_completed'] = DownloadTask.objects.filter(
        user=request.user,
        status='completed',
        completed_at__gte=recent_cutoff
    ).count()
    
    return JsonResponse(stats)
