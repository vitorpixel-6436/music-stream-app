from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, JsonResponse, HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from .models import MusicFile, Artist, Album
import os
import mimetypes
import logging

logger = logging.getLogger(__name__)


def index(request):
    """Display homepage with music list"""
    music_files = MusicFile.objects.all().order_by('-created_at')
    context = {'music_files': music_files}
    return render(request, 'music/index.html', context)


def player(request, pk):
    """Display music player for specific track"""
    music_file = get_object_or_404(MusicFile, pk=pk)
    
    # Increment play count
    try:
        music_file.increment_play_count()
    except Exception as e:
        logger.error(f'Error updating play count: {e}')
    
    context = {'music_file': music_file}
    return render(request, 'music/player.html', context)


@require_http_methods(["GET"])
def stream_music(request, pk):
    """Stream music file"""
    music_file = get_object_or_404(MusicFile, pk=pk)

    if not music_file.file:
        raise Http404('Audio file not found')

    file_path = music_file.file.path
    content_type, _ = mimetypes.guess_type(file_path)

    response = FileResponse(open(file_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
    return response


@require_http_methods(["GET"])
def download_music(request, pk):
    """Download music file"""
    music_file = get_object_or_404(MusicFile, pk=pk)

    if not music_file.file:
        raise Http404('Audio file not found')

    # Increment download count
    try:
        music_file.increment_download_count()
    except Exception as e:
        logger.error(f'Error updating download count: {e}')

    file_path = music_file.file.path
    content_type, _ = mimetypes.guess_type(file_path)

    response = FileResponse(open(file_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    return response


@require_http_methods(["POST"])
def upload_music(request):
    """Upload new music file"""
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file provided'}, status=400)

    file = request.FILES['file']
    title = request.POST.get('title', file.name)
    artist_name = request.POST.get('artist', 'Unknown Artist')
    album_name = request.POST.get('album', '')

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

        # Determine file format
        file_ext = os.path.splitext(file.name)[1][1:].lower()
        format_map = {
            'mp3': 'mp3',
            'flac': 'flac',
            'ogg': 'ogg',
            'm4a': 'm4a',
            'wav': 'wav'
        }
        file_format = format_map.get(file_ext, 'mp3')

        music_file = MusicFile.objects.create(
            title=title,
            artist=artist,
            album=album,
            file=file,
            format=file_format,
            file_size=file.size
        )

        return JsonResponse({
            'id': str(music_file.id),
            'title': music_file.title,
            'artist': music_file.artist.name,
            'message': 'File uploaded successfully'
        })
    
    except Exception as e:
        logger.error(f'Error uploading file: {e}')
        return JsonResponse({'error': 'Upload failed'}, status=500)


def upload_page(request):
    """Display upload form"""
    return render(request, 'music/upload.html')


# Error handlers
def handler404(request, exception):
    """Handle 404 errors gracefully"""
    context = {'error_message': 'Page not found (404)'}
    return render(request, 'music/404.html', context, status=404)


def handler500(request):
    """Handle 500 errors gracefully"""
    logger.error('Internal Server Error (500)')
    context = {'error_message': 'Internal server error (500)'}
    return render(request, 'music/500.html', context, status=500)
