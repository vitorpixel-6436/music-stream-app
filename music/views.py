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
    music_files = MusicFile.objects.select_related('artist', 'album').all()
    
    # Search functionality with sanitization
    search_query = request.GET.get('q', '').strip()
    if search_query:
        safe_query = escape(search_query)
        music_files = music_files.filter(
            Q(title__icontains=safe_query) |
            Q(artist__name__icontains=safe_query) |
            Q(album__title__icontains=safe_query)
        )
    
    # Filter by artist
    artist_filter = request.GET.get('artist', '').strip()
    if artist_filter:
        music_files = music_files.filter(artist__id=artist_filter)
    
    # Sort options
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['-created_at', 'title', '-title', 'artist__name', '-play_count']
    if sort_by in valid_sorts:
        music_files = music_files.order_by(sort_by)
    else:
        music_files = music_files.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(music_files, PAGES_PER_PAGE)
    page = request.GET.get('page')
    try:
        music_files = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        music_files = paginator.page(1)
    
    # Get filters data
    all_artists = Artist.objects.all().order_by('name')
    
    context = {
        'music_files': music_files,
        'search_query': search_query,
        'selected_artist': artist_filter,
        'sort_by': sort_by,
        'all_artists': all_artists,
    }
    return render(request, 'music/index.html', context)

def player(request, pk):
    """Display music player for specific track"""
    music_file = get_object_or_404(MusicFile.objects.select_related('artist', 'album'), pk=pk)
    
    # Async-like play count increment
    try:
        music_file.increment_play_count()
    except Exception as e:
        logger.error(f"Failed to increment play count for {pk}: {e}")
    
    # Optimized recommendations
    recommendations = MusicFile.objects.filter(artist=music_file.artist).exclude(id=pk)[:5]
    if not recommendations.exists():
        recommendations = MusicFile.objects.exclude(id=pk).order_by('?')[:5]
    
    context = {
        'music_file': music_file,
        'recommendations': recommendations,
    }
    return render(request, 'music/player.html', context)

@require_http_methods(["GET"])
def stream_music(request, pk):
    """Stream music file with byte-range support readiness"""
    music_file = get_object_or_404(MusicFile, pk=pk)
    if not music_file.file or not os.path.exists(music_file.file.path):
        raise Http404("Audio file not found on server")
    
    file_path = music_file.file.path
    content_type, _ = mimetypes.guess_type(file_path)
    
    # FileResponse handles streaming and range requests efficiently
    response = FileResponse(open(file_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
    response['Accept-Ranges'] = 'bytes'
    response['X-Content-Type-Options'] = 'nosniff'
    return response

@require_http_methods(["GET"])
def download_music(request, pk):
    """Download music file with tracking"""
    music_file = get_object_or_404(MusicFile, pk=pk)
    if not music_file.file:
        raise Http404("Audio file not found")
    
    try:
        music_file.increment_download_count()
    except Exception as e:
        logger.error(f"Download tracking error: {e}")
        
    response = FileResponse(open(music_file.file.path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(music_file.file.path)}"'
    return response

@require_http_methods(["POST"])
def upload_music(request):
    """Secure AJAX upload endpoint"""
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file provided'}, status=400)
    
    file = request.FILES['file']
    if file.size > 50 * 1024 * 1024:
        return JsonResponse({'error': 'File too large (max 50MB)'}, status=400)
        
    title = escape(request.POST.get('title', file.name))
    artist_name = escape(request.POST.get('artist', 'Unknown Artist'))
    
    try:
        artist, _ = Artist.objects.get_or_create(name=artist_name)
        
        # File extension validation
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in ['.mp3', '.flac', '.ogg', '.wav', '.m4a']:
            return JsonResponse({'error': 'Unsupported file format'}, status=400)
            
        music_file = MusicFile.objects.create(
            title=title,
            artist=artist,
            file=file,
            format=ext[1:]
        )
        
        return JsonResponse({
            'id': str(music_file.id),
            'title': music_file.title,
            'message': 'Upload successful'
        })
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return JsonResponse({'error': 'Internal server error during upload'}, status=500)

def upload_page(request):
    return render(request, 'music/upload.html')

def api_search(request):
    query = escape(request.GET.get('q', '').strip())
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    results = MusicFile.objects.filter(
        Q(title__icontains=query) | Q(artist__name__icontains=query)
    ).values('id', 'title', 'artist__name')[:10]
    
    return JsonResponse({'results': list(results)})


def handler404(request, exception):
    return render(request, 'music/404.html', status=404)

def handler500(request):
    return render(request, 'music/500.html', status=500)
