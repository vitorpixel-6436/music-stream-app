"""
Download Management Views
=========================

Comprehensive views for managing download tasks.
Separated from main views.py for better code organization.

Features:
- URL submission and validation
- Real-time progress tracking via AJAX
- Download history with filters
- Task cancellation
- Permission checks
- Automatic background processing
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import DownloadTask
from .forms import URLImportForm
from .tasks import process_download_task_async, cancel_task_processing, process_pending_downloads
import logging

logger = logging.getLogger(__name__)


def get_request_user(request):
    """Get current user or create/get anonymous user for testing."""
    if request.user.is_authenticated:
        return request.user
    
    # Get or create anonymous user for testing
    user, _ = User.objects.get_or_create(
        username='anonymous',
        defaults={
            'email': 'anonymous@test.com',
            'is_active': True
        }
    )
    return user


@require_http_methods(["GET", "POST"])
def download_create(request):
    """
    Handle new download task creation.
    
    GET: Display form
    POST: Submit URL and create download task
    """
    user = get_request_user(request)
    
    if request.method == 'POST':
        form = URLImportForm(request.POST)
        
        if form.is_valid():
            try:
                # Create download task
                task = DownloadTask.objects.create(
                    user=user,
                    url=form.cleaned_data['url'],
                    output_format=form.cleaned_data.get('output_format', 'mp3'),
                    output_quality=form.cleaned_data.get('output_quality', '320k'),
                    status='pending'
                )
                
                # Determine source type from URL
                url_lower = task.url.lower()
                if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
                    task.source_type = 'youtube'
                elif 'soundcloud.com' in url_lower:
                    task.source_type = 'soundcloud'
                elif 'bandcamp.com' in url_lower:
                    task.source_type = 'bandcamp'
                else:
                    task.source_type = 'url'
                task.save(update_fields=['source_type'])
                
                # Log task creation
                logger.info(
                    f"Download task created: {task.id} by {user.username} - {task.url}"
                )
                
                # Start background processing immediately
                try:
                    process_download_task_async(str(task.id))
                    logger.info(f"Started background processing for task {task.id}")
                except Exception as e:
                    logger.error(f"Failed to start background task: {e}")
                    # Task will be picked up by process_pending_downloads() later
                
                messages.success(
                    request, 
                    f'✅ Download started! Task ID: {str(task.id)[:8]}'
                )
                
                # Return JSON for AJAX requests
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'task_id': str(task.id),
                        'message': 'Download task created and started',
                        'redirect_url': '/downloads/'  # FIXED: was /music/downloads/
                    })
                
                return redirect('music:download_manager')
                
            except Exception as e:
                logger.error(f"Download task creation error: {e}", exc_info=True)
                messages.error(request, f'❌ Error creating download task: {str(e)}')
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': str(e)
                    }, status=500)
        else:
            # Form validation errors
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
    else:
        form = URLImportForm()
    
    context = {
        'form': form,
        'page_title': 'Import from URL',
    }
    return render(request, 'music/download_create.html', context)


@require_http_methods(["GET"])
def download_status_api(request, task_id):
    """
    API endpoint for checking download task status.
    Returns JSON with current progress and status.
    
    Used by frontend for real-time progress updates.
    """
    user = get_request_user(request)
    
    try:
        task = get_object_or_404(
            DownloadTask,
            id=task_id,
            user=user
        )
        
        response_data = {
            'success': True,
            'task_id': str(task.id),
            'status': task.status,
            'progress': task.progress,
            'current_step': task.current_step,
            'is_active': task.is_active,
            'error_message': task.error_message if task.status == 'failed' else None,
        }
        
        # Add result track info if completed
        if task.status == 'completed' and task.result_track:
            response_data['result'] = {
                'id': str(task.result_track.id),
                'title': task.result_track.title,
                'artist': task.result_track.artist.name,
                'url': f'/music/player/{task.result_track.id}/'
            }
        
        # Add timing info
        if task.started_at:
            response_data['elapsed_seconds'] = task.elapsed_time
        
        return JsonResponse(response_data)
        
    except DownloadTask.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Task not found or access denied'
        }, status=404)
    except Exception as e:
        logger.error(f"Status API error for task {task_id}: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)


@require_http_methods(["GET"])
def download_list(request):
    """
    List all download tasks for current user with filtering and pagination.
    Also processes any pending downloads.
    """
    user = get_request_user(request)
    
    # Process pending downloads in background
    try:
        process_pending_downloads(max_concurrent=3)
    except Exception as e:
        logger.error(f"Error processing pending downloads: {e}")
    
    # Base queryset
    tasks = DownloadTask.objects.filter(user=user).select_related(
        'result_track', 'result_track__artist'
    )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter and status_filter != 'all':
        tasks = tasks.filter(status=status_filter)
    
    # Filter by source type
    source_filter = request.GET.get('source', '')
    if source_filter and source_filter != 'all':
        tasks = tasks.filter(source_type=source_filter)
    
    # Search by URL or title
    search_query = request.GET.get('q', '').strip()
    if search_query:
        tasks = tasks.filter(
            Q(url__icontains=search_query) |
            Q(original_title__icontains=search_query) |
            Q(original_artist__icontains=search_query)
        )
    
    # Sort
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['-created_at', 'created_at', '-completed_at', 'status']
    if sort_by in valid_sorts:
        tasks = tasks.order_by(sort_by)
    else:
        tasks = tasks.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(tasks, 20)  # 20 tasks per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    stats = {
        'total': tasks.count(),
        'active': DownloadTask.objects.filter(
            user=user,
            status__in=['pending', 'downloading', 'processing']
        ).count(),
        'completed': DownloadTask.objects.filter(
            user=user,
            status='completed'
        ).count(),
        'failed': DownloadTask.objects.filter(
            user=user,
            status='failed'
        ).count(),
    }
    
    context = {
        'page_obj': page_obj,
        'tasks': page_obj.object_list,
        'stats': stats,
        'status_filter': status_filter,
        'source_filter': source_filter,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    
    return render(request, 'music/download_list.html', context)


@require_POST
def download_cancel(request, task_id):
    """
    Cancel an active download task.
    Only works for pending/downloading tasks.
    """
    user = get_request_user(request)
    
    try:
        task = get_object_or_404(
            DownloadTask,
            id=task_id,
            user=user
        )
        
        # Check if task can be cancelled
        if not task.is_active:
            messages.warning(request, 'Task cannot be cancelled (already completed or failed)')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': 'Task is not active'
                }, status=400)
            
            return redirect('music:download_manager')
        
        # Cancel processing thread
        cancel_task_processing(str(task.id))
        
        # Mark as cancelled in DB
        task.status = 'cancelled'
        task.completed_at = timezone.now()
        task.save(update_fields=['status', 'completed_at'])
        
        logger.info(f"Download task {task.id} cancelled by {user.username}")
        
        messages.success(request, '✅ Download task cancelled')
        
        # Return JSON for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Task cancelled successfully'
            })
        
        return redirect('music:download_manager')
        
    except DownloadTask.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': 'Task not found'
            }, status=404)
        
        messages.error(request, 'Download task not found')
        return redirect('music:download_manager')
    except Exception as e:
        logger.error(f"Cancel error for task {task_id}: {e}")
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
        
        messages.error(request, f'Error cancelling task: {str(e)}')
        return redirect('music:download_manager')


@require_POST
def download_retry(request, task_id):
    """
    Retry a failed download task.
    Creates a new task with same parameters and starts processing.
    """
    user = get_request_user(request)
    
    try:
        old_task = get_object_or_404(
            DownloadTask,
            id=task_id,
            user=user,
            status='failed'
        )
        
        # Create new task with same parameters
        new_task = DownloadTask.objects.create(
            user=user,
            url=old_task.url,
            source_type=old_task.source_type,
            output_format=old_task.output_format,
            output_quality=old_task.output_quality,
            status='pending'
        )
        
        logger.info(
            f"Retry task created: {new_task.id} (original: {old_task.id})"
        )
        
        # Start processing immediately
        try:
            process_download_task_async(str(new_task.id))
        except Exception as e:
            logger.error(f"Failed to start retry task: {e}")
        
        messages.success(
            request,
            f'✅ Download task retried! New task ID: {str(new_task.id)[:8]}'
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'new_task_id': str(new_task.id),
                'message': 'Task retry successful'
            })
        
        return redirect('music:download_manager')
        
    except Exception as e:
        logger.error(f"Retry error for task {task_id}: {e}")
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
        
        messages.error(request, f'Error retrying task: {str(e)}')
        return redirect('music:download_manager')


@require_http_methods(["GET"])
def download_bulk_status(request):
    """
    Get status of multiple tasks at once.
    Optimized for polling multiple tasks with one request.
    
    Query params: task_ids (comma-separated)
    Example: /api/downloads/bulk-status/?task_ids=uuid1,uuid2,uuid3
    """
    user = get_request_user(request)
    
    try:
        task_ids_str = request.GET.get('task_ids', '')
        if not task_ids_str:
            return JsonResponse({
                'success': False,
                'error': 'No task IDs provided'
            }, status=400)
        
        task_ids = [tid.strip() for tid in task_ids_str.split(',') if tid.strip()]
        
        # Limit to 50 tasks per request
        if len(task_ids) > 50:
            return JsonResponse({
                'success': False,
                'error': 'Too many task IDs (max 50)'
            }, status=400)
        
        tasks = DownloadTask.objects.filter(
            id__in=task_ids,
            user=user
        ).select_related('result_track', 'result_track__artist')
        
        results = []
        for task in tasks:
            task_data = {
                'task_id': str(task.id),
                'status': task.status,
                'progress': task.progress,
                'current_step': task.current_step,
                'is_active': task.is_active,
            }
            
            if task.status == 'completed' and task.result_track:
                task_data['result'] = {
                    'id': str(task.result_track.id),
                    'title': task.result_track.title,
                    'artist': task.result_track.artist.name,
                }
            
            results.append(task_data)
        
        return JsonResponse({
            'success': True,
            'tasks': results,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Bulk status error: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)
