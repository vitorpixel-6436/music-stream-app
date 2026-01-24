from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from .models import Track
import os
import mimetypes


def index(request):
    """Display homepage with music list"""
    music_files = Track.objects.all().order_by('-uploaded_at')
    context = {'music_files': music_files}
    return render(request, 'music/index.html', context)


def player(request, pk):
    """Display music player for specific track"""
    music_file = get_object_or_404(Track, pk=pk)
    context = {'music_file': music_file}
    return render(request, 'music/player.html', context)


@require_http_methods(["GET"])
def stream_music(request, pk):
    """Stream music file"""
    music_file = get_object_or_404(Track, pk=pk)
    
    if not music_file.file:
        return HttpResponse(status=404)
    
    file_path = music_file.file.path
    content_type, _ = mimetypes.guess_type(file_path)
    
    response = FileResponse(open(file_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
    return response


@require_http_methods(["GET"])
def download_music(request, pk):
    """Download music file"""
    music_file = get_object_or_404(Track, pk=pk)
    
    if not music_file.file:
        return HttpResponse(status=404)
    
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
    artist = request.POST.get('artist', '')
    album = request.POST.get('album', '')
    
    music_file = Track.objects.create(
        title=title,
        artist=artist,
        album=album,
        file=file
    )
    
    return JsonResponse({
        'id': music_file.id,
        'title': music_file.title,
        'artist': music_file.artist,
        'message': 'File uploaded successfully'
    })


def upload_page(request):
    """Display upload form"""
    return render(request, 'music/upload.html')
