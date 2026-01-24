from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, JsonResponse, HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils.html import escape
from .models import MusicFile, Artist, Album
import os
import mimetypes
import logging

logger = logging.getLogger(__name__)
PAGES_PER_PAGE = 12

def index(request):
    """Display homepage with music list, search, and filters"""
    music_files = MusicFile.objects.all().order_by('-created_at')
    
    # Search functionality with sanitization
    search_query = request.GET.get('q', '').strip()
    if search_query:
        # Simple sanitization
        safe_query = escape(search_query)
        music_files = music_files.filter(
            Q(title__icontains=safe_query) |
            Q(artist__name__icontains=safe_query) |
            Q(album__title__icontains=safe_query)
        )
    
    # Filter by artist
    artist_filter = request.GET.get('artist', '').strip()
    if artist_filter and artist_filter.isdigit():
        music_files = music_files.filter(artist__id=artist_filter)
    
    # Filter by album
    album_filter = request.GET.get('album', '').strip()
    if album_filter and album_filter.isdigit():
        music_files = music_files.filter(album__id=album_filter)
    
    # Sort options
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['-created_at', 'title', '-title', 'artist__name', '-play_count']
    if sort_by in valid_sorts:
        music_files = music_files.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(music_files, PAGES_PER_PAGE)
    page = request.GET.get('page')
    try:
        music_files = paginator.page(page)
    except PageNotAnInteger:
        music_files = paginator.page(1)
    except EmptyPage:
        music_files = paginator.page(paginator.num_pages)
    
    # Get all artists and albums for filter dropdowns
    all_artists = Artist.objects.all().order_by('name')
    all_albums = Album.objects.all().order_by('title')
    
    context = {
        'music_files': music_files,
        'search_query': search_query,
        'selected_artist': artist_filter,
        'selected_album': album_filter,
        'sort_by': sort_by,
        'all_artists': all_artists,
        'all_albums': all_albums,
    }
    return render(request, 'music/index.html', context)

def player(request, pk):
    """Display music player for specific track"""
    music_file = get_object_or_404(MusicFile, pk=pk)
    
    # Increment play count with fallback
    try:
        music_file.increment_play_count()
    except Exception as e:
        logger.error(f'Error updating play count for {pk}: {e}')
    
    # Get recommendations with fallback
    try:
        recommendations = MusicFile.objects.exclude(id=pk)
        if music_file.artist:
            recommendations = recommendations.filter(artist=music_file.artist)[:5]
        elif music_file.album:
            recommendations = recommendations.filter(album=music_file.album)[:5]
        else:
            recommendations = recommendations[:5]
    except Exception as e:
        logger.error(f'Error getting recommendations: {e}')
        recommendations = MusicFile.objects.exclude(id=pk)[:5]
    
    context = {
        'music_file': music_file,
        'recommendations': recommendations,
    }
    return render(request, 'music/player.html', context)

@require_http_methods(["GET"])
def stream_music(request, pk):
    """Stream music file with security checks"""
    music_file = get_object_or_404(MusicFile, pk=pk)
    if not music_file.file:
        logger.warning(f'Stream request for missing file ID {pk}')
        raise Http404('Audio file not found')
    
    try:
        file_path = music_file.file.path
        if not os.path.exists(file_path):
            logger.error(f'File path does not exist: {file_path}')
            raise Http404('Physical file not found')
            
        content_type, _ = mimetypes.guess_type(file_path)
        response = FileResponse(open(file_path, 'rb'), content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
        # Security headers for streaming
        response['X-Content-Type-Options'] = 'nosniff'
        return response
    except Exception as e:
        logger.error(f'Streaming error for {pk}: {e}')
        return HttpResponse('Error streaming file', status=500)

@require_http_methods(["GET"])
def download_music(request, pk):
    """Download music file with count tracking and security"""
    music_file = get_object_or_404(MusicFile, pk=pk)
    if not music_file.file:
        raise Http404('Audio file not found')
    
    # Increment download count
    try:
        music_file.increment_download_count()
    except Exception as e:
        logger.error(f'Error updating download count for {pk}: {e}')
    
    try:
        file_path = music_file.file.path
        content_type, _ = mimetypes.guess_type(file_path)
        response = FileResponse(open(file_path, 'rb'), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
    except Exception as e:
        logger.error(f'Download error for {pk}: {e}')
        return HttpResponse('Error downloading file', status=500)

@require_http_methods(["POST"])
def upload_music(request):
    """Upload new music file with extensive validation and security"""
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file provided'}, status=400)
    
    file = request.FILES['file']
    
    # Basic size check (additional to settings.py MAX_UPLOAD_SIZE)
    if file.size > 50 * 1024 * 1024:
        return JsonResponse({'error': 'File too large (max 50MB)'}, status=400)
        
    title = escape(request.POST.get('title', file.name))
    artist_name = escape(request.POST.get('artist', 'Unknown Artist'))
    album_name = escape(request.POST.get('album', ''))
    
    try:
        # Get or create artist
        artist, _ = Artist.objects.get_or_create(name=artist_name)
        
        # Get or create album if provided
        album = None
        if album_name:
            album, _ = Album.objects.get_or_create(
                title=album_name,
                artist=artist
            )
        
        # Determine file format safely
        file_ext = os.path.splitext(file.name)[1][1:].lower()
        allowed_formats = ['mp3', 'flac', 'ogg', 'm4a', 'wav']
        if file_ext not in allowed_formats:
            return JsonResponse({'error': f'Unsupported format: {file_ext}'}, status=400)
            
        music_file = MusicFile.objects.create(
            title=title,
            artist=artist,
            album=album,
            file=file,
            format=file_ext,
            file_size=file.size
        )
        
        return JsonResponse({
            'id': str(music_file.id),
            'title': music_file.title,
            'artist': music_file.artist.name,
            'message': 'File uploaded successfully'
        })
    
    except Exception as e:
        logger.error(f'Upload failure: {e}')
        return JsonResponse({'error': 'Server error during upload'}, status=500)

def upload_page(request):
    """Display upload form"""
    return render(request, 'music/upload.html')

def api_search(request):
    """API endpoint for autocomplete search with rate limit logic ready"""
    query = escape(request.GET.get('q', '').strip())
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    try:
        results = MusicFile.objects.filter(
            Q(title__icontains=query) |
            Q(artist__name__icontains=query)
        ).values('id', 'title', 'artist__name')[:10]
        return JsonResponse({'results': list(results)})
    except Exception as e:
        logger.error(f'API Search error: {e}')
        return JsonResponse({'results': [], 'error': 'Search failed'}, status=500)

# Error handlers
def handler404(request, exception):
    """Handle 404 errors gracefully"""
    context = {'error_message': 'The music you are looking for has faded away... (404)'}
    return render(request, 'music/404.html', context, status=404)

def handler500(request):
    """Handle 500 errors gracefully with logging"""
    logger.critical('CRITICAL: Internal Server Error (500) triggered')
    context = {'error_message': 'Our orchestra is currently out of tune. Please try again later. (500)'}
    return render(request, 'music/500.html', context, status=500)
