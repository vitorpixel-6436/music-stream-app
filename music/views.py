from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, JsonResponse, HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.base import ContentFile
from django.db.models import Q
from django.utils.html import escape
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import MusicFile, Artist, Album, Genre, DownloadTask
from .forms import URLImportForm
import os
import mimetypes
import logging

try:
    from mutagen import File as MutagenFile
    from mutagen.id3 import ID3, APIC
    from mutagen.mp3 import MP3
    from mutagen.flac import FLAC
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False
    logging.warning('Mutagen not installed. Metadata extraction disabled.')

logger = logging.getLogger(__name__)
PAGES_PER_PAGE = 12

def extract_metadata(file_path):
    """Extract metadata from audio file using mutagen"""
    if not MUTAGEN_AVAILABLE:
        return {}
    
    try:
        audio = MutagenFile(file_path, easy=True)
        if audio is None:
            return {}
        
        metadata = {
            'title': audio.get('title', [None])[0],
            'artist': audio.get('artist', [None])[0] or audio.get('albumartist', [None])[0],
            'album': audio.get('album', [None])[0],
            'year': audio.get('date', [None])[0],
            'genre': audio.get('genre', [None])[0],
        }
        
        # Extract album art
        try:
            audio_full = MutagenFile(file_path)
            if hasattr(audio_full, 'tags'):
                for key in audio_full.tags.keys():
                    if key.startswith('APIC'):
                        artwork = audio_full.tags[key]
                        metadata['artwork'] = artwork.data
                        metadata['artwork_mime'] = artwork.mime
                        break
        except Exception as e:
            logger.debug(f"Could not extract artwork: {e}")
        
        return {k: v for k, v in metadata.items() if v}
    except Exception as e:
        logger.error(f"Metadata extraction error: {e}")
        return {}

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
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 100 * 1024 * 1024)
    if file.size > max_size:
        return JsonResponse({'error': f'File too large (max {max_size // (1024*1024)}MB)'}, status=400)
        
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
    """Handle music upload page with form processing and metadata extraction"""
    if request.method == 'POST':
        try:
            # Validate file presence
            if 'file' not in request.FILES:
                messages.error(request, 'Файл не выбран')
                return render(request, 'music/upload.html')
            
            file = request.FILES['file']
            
            # File size validation using settings
            max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 100 * 1024 * 1024)
            if file.size > max_size:
                max_size_mb = max_size // (1024 * 1024)
                messages.error(request, f'Файл слишком большой (максимум {max_size_mb}MB). Размер файла: {file.size // (1024*1024)}MB')
                return render(request, 'music/upload.html')
            
            # File format validation
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in ['.mp3', '.flac', '.ogg', '.wav', '.m4a']:
                messages.error(request, f'Неподдерживаемый формат: {ext}')
                return render(request, 'music/upload.html')
            
            # Save file temporarily to extract metadata
            temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, file.name)
            
            with open(temp_path, 'wb+') as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)
            
            # Extract metadata from file
            metadata = extract_metadata(temp_path)
            logger.info(f"Extracted metadata: {metadata.keys()}")
            
            # Get form data with fallback to extracted metadata
            title = escape(request.POST.get('title', '').strip()) or metadata.get('title') or os.path.splitext(file.name)[0]
            artist_name = escape(request.POST.get('artist', '').strip()) or metadata.get('artist') or 'Unknown Artist'
            album_name = escape(request.POST.get('album', '').strip()) or metadata.get('album', '')
            year = request.POST.get('year', '').strip() or (metadata.get('year', '')[:4] if metadata.get('year') else '')
            genre_names = request.POST.getlist('genres') or ([metadata.get('genre')] if metadata.get('genre') else [])
            
            if not title:
                messages.error(request, 'Название трека обязательно')
                os.remove(temp_path)
                return render(request, 'music/upload.html')
            
            # Create or get artist
            artist, _ = Artist.objects.get_or_create(name=artist_name)
            
            # Create or get album if provided
            album = None
            if album_name:
                album_data = {'title': album_name}
                if year and year.isdigit():
                    album_data['year'] = int(year)
                album, _ = Album.objects.get_or_create(
                    title=album_name,
                    artist=artist,
                    defaults=album_data
                )
            
            # Get or create genre (first one from the list)
            genre = None
            if genre_names and genre_names[0]:
                genre, _ = Genre.objects.get_or_create(name=genre_names[0])
            
            # Reset file pointer
            file.seek(0)
            
            # Create music file
            music_file = MusicFile.objects.create(
                title=title,
                artist=artist,
                album=album,
                genre=genre,
                file=file,
                format=ext[1:]
            )
            
            # Handle manually uploaded cover image FIRST (priority)
            if 'cover' in request.FILES:
                cover_file = request.FILES['cover']
                if cover_file.size <= 5 * 1024 * 1024:  # 5MB max for images
                    music_file.cover_image = cover_file
                    music_file.save(update_fields=['cover_image'])
                    logger.info(f"Saved manual cover image for {music_file.id}")
            
            # Handle embedded artwork from metadata (fallback)
            elif 'artwork' in metadata and 'artwork_mime' in metadata:
                try:
                    artwork_ext = metadata['artwork_mime'].split('/')[-1]
                    if artwork_ext == 'jpeg':
                        artwork_ext = 'jpg'
                    filename = f"{music_file.id}_cover.{artwork_ext}"
                    music_file.cover_image.save(filename, ContentFile(metadata['artwork']), save=True)
                    logger.info(f"Saved embedded artwork for {music_file.id}")
                except Exception as e:
                    logger.error(f"Failed to save embedded artwork: {e}")
            
            # Clean up temp file
            try:
                os.remove(temp_path)
            except:
                pass
            
            messages.success(request, f'✅ Трек "{title}" успешно загружен!')
            return redirect('music:index')
            
        except Exception as e:
            logger.error(f"Upload error in upload_page: {e}", exc_info=True)
            messages.error(request, f'Ошибка загрузки: {str(e)}')
            try:
                if 'temp_path' in locals() and os.path.exists(temp_path):
                    os.remove(temp_path)
            except:
                pass
            return render(request, 'music/upload.html')
    
    return render(request, 'music/upload.html')


@login_required
def url_import(request):
    """Handle URL import with enhanced validation"""
    if request.method == 'POST':
        form = URLImportForm(request.POST)
        if form.is_valid():
            try:
                # Create download task
                task = DownloadTask.objects.create(
                    user=request.user,
                    url=form.cleaned_data['url'],
                    source_type=form.cleaned_data.get('source_type', 'url'),
                    output_format=form.cleaned_data.get('output_format', 'mp3'),
                    output_quality=form.cleaned_data.get('output_quality', '320k')
                )
                
                # Queue background download
                from .tasks import process_download_task
                process_download_task.delay(str(task.id))
                
                messages.success(request, f'Download task created: {task.id}')
                return redirect('download_manager')
            except Exception as e:
                logger.error(f"URL import error: {e}")
                messages.error(request, 'Failed to create download task')
        else:
            messages.error(request, 'Invalid URL format')
    else:
        form = URLImportForm()
    
    return render(request, 'music/url_import.html', {'form': form})


@login_required
def download_manager(request):
    """Display user's download tasks"""
    tasks = DownloadTask.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'tasks': tasks,
        'active_count': tasks.filter(status__in=['pending', 'downloading', 'processing']).count(),
    }
    return render(request, 'music/download_manager.html', context)


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
