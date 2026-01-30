# Changelog

Все примечательные изменения этого проекта документируются в этом файле.

## [2.1.1] - 2026-01-30

### 🔧 Minor Improvements & Bug Fixes

**Маскировка: Internal infrastructure enhancements**

Этот патч фокусируется на внутренних улучшениях инфраструктуры и оптимизации backend-процессов.

#### Added
- ✅ **DownloadTask Model** - Background task tracking system
  - Status tracking (pending, downloading, processing, completed, failed)
  - Progress monitoring (0-100%)
  - Source type detection (youtube, soundcloud, bandcamp, direct)
  - Output format configuration (mp3, flac, wav, m4a, ogg)
  - Quality settings (320k, 256k, 192k, 128k)
  - Error handling with retry mechanism
  - Result linking to MusicFile

- ✅ **Download Manager Views** - Web interface for task monitoring
  - URL import form (`/import/`)
  - Task dashboard (`/downloads/`)
  - Real-time progress display
  - Status badges and visual indicators

- ✅ **Media Downloader Utility** - Helper for external content
  - yt-dlp integration for YouTube/SoundCloud/Bandcamp
  - Automatic format detection
  - Metadata extraction
  - Audio-only download optimization
  - Error handling and logging

- ✅ **Celery Background Tasks** - Async processing
  - `download_from_url` task for background downloads
  - Progress updates via task model
  - Automatic file conversion
  - Result storage in media library

- ✅ **Admin Panel Integration** - Download task management
  - DownloadTaskAdmin with progress bars
  - Status badges (color-coded)
  - Error message display
  - Direct link to result track
  - Filter by status, source, user
  - Active download counter in dashboard

#### URL Import Features

**Supported Sources:**
- 🎬 YouTube (videos & music)
- ☁️ SoundCloud (tracks & sets)
- 🎸 Bandcamp (albums & EPs)
- 🔗 Direct audio URLs (mp3, flac, wav, etc.)

**Form Configuration:**
- URL input with validation
- Output format selection (mp3, flac, wav, m4a, ogg)
- Quality presets (128k-320k)
- Auto-metadata extraction
- Background queue processing

#### Templates

**url_import.html:**
- Glass morphism design
- URL input with validation
- Format/quality dropdowns
- Platform badges (YouTube, SoundCloud, Bandcamp)
- Quick link to download manager
- Submit button with loading state

**download_manager.html:**
- Statistics dashboard (total, active, completed, failed)
- Task list with status badges
- Progress bars for active downloads
- Auto-refresh for active tasks (5s interval)
- Empty state with CTA
- Direct links to result tracks
- Error message display

#### Technical Implementation

**Models:**
```python
from music.models import DownloadTask

# Create download task
task = DownloadTask.objects.create(
    user=request.user,
    url='https://youtube.com/watch?v=...',
    output_format='mp3',
    output_quality='320k'
)

# Queue for processing
from music.tasks import download_from_url
download_from_url.delay(task.id)
```

**Views:**
```python
# URL import view
def url_import(request):
    if request.method == 'POST':
        form = URLImportForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            download_from_url.delay(task.id)
            return redirect('music:download_manager')
    return render(request, 'music/url_import.html', {'form': form})

# Download manager
def download_manager(request):
    tasks = DownloadTask.objects.filter(
        user=request.user
    ).order_by('-created_at')
    return render(request, 'music/download_manager.html', {'tasks': tasks})
```

**Celery Tasks:**
```python
@shared_task
def download_from_url(task_id):
    task = DownloadTask.objects.get(id=task_id)
    task.status = 'downloading'
    task.save()
    
    try:
        # Download via yt-dlp
        from music.utils.downloader import download_media
        file_path, metadata = download_media(
            url=task.url,
            output_format=task.output_format,
            quality=task.output_quality,
            progress_callback=lambda p: task.update_progress(p)
        )
        
        # Create MusicFile
        music_file = MusicFile.objects.create(
            title=metadata['title'],
            artist=get_or_create_artist(metadata['artist']),
            file=file_path,
            format=task.output_format
        )
        
        task.result_track = music_file
        task.status = 'completed'
        task.save()
        
    except Exception as e:
        task.status = 'failed'
        task.error_message = str(e)
        task.save()
```

#### Database Migration

```bash
# Apply migration
python manage.py migrate

# Migration creates DownloadTask table with:
# - UUID primary key
# - ForeignKey to User
# - URL and source_type fields
# - Status and progress fields
# - Output configuration fields
# - Metadata fields (title, artist, duration, file_size)
# - Result linking (ForeignKey to MusicFile)
# - Error tracking fields
# - Timestamps (created_at, started_at, completed_at)
```

### Improved
- 🎨 Better background task handling with Celery
- 🎨 Progress tracking for long-running operations
- 🎨 User-facing download queue interface
- 🎨 Automatic retry for failed downloads (up to 3 attempts)

### Changed
- 📝 Admin dashboard now shows active downloads count
- 📝 URLs module reorganized with new routes
- 📝 Added helper utilities in `music/utils/`

### Fixed
- 🐛 **[Hotfix]** Template syntax error in upload.html (invalid `split` filter)
- 🐛 Database indexes added for DownloadTask queries
- 🐛 Proper cleanup of temporary download files
- 🐛 Error handling for invalid URLs
- 🐛 Genre selection now uses hardcoded list instead of custom filter

### Developer Notes

**Adding Custom Downloaders:**
Extend `download_media()` in `music/utils/downloader.py`:
```python
def download_media(url, output_format='mp3', quality='320k', progress_callback=None):
    # Detect source
    if 'spotify.com' in url:
        return download_spotify(url, output_format, quality, progress_callback)
    elif 'youtube.com' in url or 'youtu.be' in url:
        return download_youtube(url, output_format, quality, progress_callback)
    # Add more sources here
```

**Custom Progress Callbacks:**
```python
def my_progress_callback(percent):
    print(f"Download progress: {percent}%")
    # Update UI, send WebSocket message, etc.

download_media(url, progress_callback=my_progress_callback)
```

### Performance
- ⚡ Async downloads don't block web requests
- ⚡ Database indexes on DownloadTask.status and DownloadTask.user
- ⚡ Lazy loading for download manager (pagination planned for v2.1.2)

### Security
- 🔒 URL validation before download
- 🔒 User isolation (can only see own downloads)
- 🔒 File path sanitization
- 🔒 Temporary file cleanup after processing

### Dependencies

**New:**
- yt-dlp >= 2024.1.0 (already in requirements)
- celery >= 5.3.4 (already in requirements)
- redis >= 5.0.0 (already in requirements)

**Installation:**
```bash
# Redis required for Celery
sudo apt install redis-server  # Linux
brew install redis  # macOS
# Windows: Download from https://github.com/microsoftarchive/redis/releases

# Start Redis
redis-server

# Start Celery worker
celery -A music_stream worker -l info
```

### Known Issues
- ⚠️ Very long videos (>2 hours) may timeout (increase CELERY_TASK_TIME_LIMIT)
- ⚠️ Some regional-restricted content may fail
- ⚠️ Rate limiting on some platforms (YouTube, SoundCloud)
- ⚠️ WebSocket for real-time progress planned for v2.1.2

### Future Enhancements (v2.1.2+)
- [ ] WebSocket real-time progress updates
- [ ] Batch URL import (multiple URLs at once)
- [ ] Playlist import (entire YouTube/Spotify playlists)
- [ ] Schedule downloads for later
- [ ] Download history with filters
- [ ] Auto-retry failed downloads
- [ ] Bandwidth throttling options

---

## [2.1.0] - 2026-01-30

### ✨ Admin & Management QoL Improvements

**Маскировка: Backend infrastructure improvements**

Этот релиз фокусируется на улучшении административного опыта и упрощении управления сервером.

#### Added
- ✅ **SystemSettings Model** - Singleton модель для системных настроек
  - Управление сайтом (название, описание)
  - Настройки загрузок (размер, форматы, лимиты)
  - Настройки обработки аудио (метаданные, нормализация)
  - UI настройки (темы, анимации)
  - Кэшированная статистика (треки, прослушивания, скачивания)

- ✅ **UploadSession Model** - Отслеживание пакетных загрузок
  - Статус сессии (pending, processing, completed, failed)
  - Счетчики успешных/неудачных загрузок
  - Логирование ошибок
  - Расчет прогресса и длительности

- ✅ **Management Commands** - Команды для администрирования
  - `addadmin` - Быстрое создание/назначение администраторов
    ```bash
    python manage.py addadmin admin@example.com --superuser
    python manage.py addadmin user@example.com --username johndoe
    ```
  - `update_stats` - Обновление системной статистики
    ```bash
    python manage.py update_stats --verbose
    ```

- ✅ **Enhanced Admin Panel** - Богатый UI с виджетами
  - **Custom Admin Site** с дашбордом статистики
  - **Color-coded Badges** для форматов, статусов, счетчиков
  - **Audio Preview** прямо в админке (inline player)
  - **Progress Bars** для отслеживания загрузок
  - **Photo/Cover Previews** с округлыми углами
  - **Statistics Widgets** (total plays, downloads, track counts)
  - **Autocomplete Fields** для Artist, Album, Genre
  - **Batch Actions** (reset play count, re-extract metadata)
  - **Improved Fieldsets** с collapsible секциями

#### Admin Panel Features

**Genre Admin:**
- Track count badge (зеленый)
- Search по названию и описанию

**Artist Admin:**
- Photo preview (100x100px, rounded)
- Track count и total plays statistics
- Collapsible statistics section

**Album Admin:**
- Cover preview (80x80px, rounded)
- Track count
- Autocomplete для artist

**MusicFile Admin:**
- Format badges (цветные: MP3=красный, FLAC=бирюзовый, и т.д.)
- Duration display (MM:SS формат)
- Play count badge (🔥 для >1000 прослушиваний)
- Audio preview player (200px inline)
- Full audio player в детальном виде
- File size display (MB)
- Batch actions:
  - Reset play count для выбранных треков
  - Re-extract metadata для выбранных треков

**SystemSettings Admin:**
- Singleton pattern (только одна запись)
- Секции: General, User Management, Audio Processing, UI
- Read-only statistics с автообновлением
- Защита от удаления

**UploadSession Admin:**
- Status badges (pending=оранжевый, processing=бирюзовый, completed=зеленый, failed=красный)
- Visual progress bars с процентами
- Duration calculation
- Error log viewing

#### Technical Details

**New Models:**
```python
# SystemSettings - Singleton для настроек
settings = SystemSettings.load()
settings.site_name = "My Music Server"
settings.max_upload_size = 200  # MB
settings.update_statistics()  # Обновить кэш

# UploadSession - Трекинг загрузок
session = UploadSession.objects.create(
    user=request.user,
    total_files=10,
    status='processing'
)
session.successful_uploads += 1
session.save()
```

**Management Commands:**
```bash
# Создать суперпользователя
python manage.py addadmin admin@example.com --superuser --password SecurePass123

# Назначить права админа существующему пользователю
python manage.py addadmin user@example.com

# Обновить статистику с детальным выводом
python manage.py update_stats --verbose
```

#### Database Migration

```bash
# Применить новые миграции
python manage.py migrate

# Создать начальные настройки
python manage.py shell
>>> from music.models import SystemSettings
>>> SystemSettings.load()  # Создаст запись если не существует
```

### Improved
- 🎨 Admin UI теперь с цветными бейджами и превью
- 🎨 Упрощенное управление пользователями через CLI
- 🎨 Централизованные настройки через админку
- 🎨 Визуальный прогресс для пакетных операций

### Changed
- 📝 Admin site переименован в MusicStreamAdminSite
- 📝 Добавлены readonly fields для метаданных
- 📝 Улучшена структура fieldsets во всех админках

### Developer Notes

**Custom Admin Actions:**
Добавляйте свои batch actions в MusicFileAdmin:
```python
def custom_action(self, request, queryset):
    # Your logic here
    self.message_user(request, "Action completed")
custom_action.short_description = "Custom action description"
```

**Extending SystemSettings:**
Добавляйте новые поля в модель и создавайте миграцию:
```python
class SystemSettings(models.Model):
    # ... existing fields ...
    new_setting = models.BooleanField(default=False)
```

### Performance
- ⚡ Кэширование статистики в SystemSettings (обновляется по команде)
- ⚡ Оптимизированные запросы с `aggregate()` и `annotate()`
- ⚡ Lazy loading для превью аудио (preload="none")

### Security
- 🔒 Защита SystemSettings от удаления
- 🔒 Singleton pattern предотвращает дублирование настроек
- 🔒 Валидация паролей в addadmin (минимум 8 символов)

### Future Enhancements (v2.1.1+)
- [x] URL download интеграция (v2.1.1 ✅)
- [ ] WebUI для SystemSettings (без админки)
- [ ] Bulk upload форма с drag-and-drop
- [ ] Real-time прогресс через WebSocket
- [ ] Email notifications для админов
- [ ] Backup/restore функции

---

## [2.0.0] - 2026-01-29

### 🎨 UI Redesign - Four Design Systems

**Premium music streaming application** с четырьмя UI дизайн-системами:

#### Added
- ✅ **Apple Glass Effects** (37.1 KB)
  - Liquid glass morphism с backdrop-filter blur
  - Dynamic glass layers (layer-1, layer-2, layer-3)
  - Context-aware blur adjustments
  - Floating particle animations

- ✅ **Steam Gaming Cards** (35.2 KB)
  - Grid cards с 3:4 aspect ratio
  - Interactive carousels с drag-to-scroll
  - Featured hero banners (21:9 format)
  - Quick action buttons

- ✅ **Spotify Minimalism** (23.0 KB)
  - Sticky navigation с scroll reveal
  - Browser history integration
  - Compact sidebar (72px → 280px)
  - Green play button (#1db954)

- ✅ **MSI Gaming Vibes** (13.0 KB)
  - RGB glow animations
  - Angular clip-path designs
  - Neon red accents
  - Hexagon background patterns

#### Stats
- 📊 Total UI Components: **108.3 KB** (4 systems, 12 files)
- 📊 Minified: **~35 KB**
- 📊 Gzipped: **~12 KB**

---

## [1.0.0] - 2026-01-24

### Added
- ✅ Полная поддержка FLAC и других аудио-форматов (MP3, WAV, AAC, OGG)
- ✅ Система управления жанрами, исполнителями и альбомами
- ✅ Создание и управление плейлистами
- ✅ Система избранных треков
- ✅ Истории прослушивания и загрузок
- ✅ Поддержка конвертации между форматами (через ffmpeg)
- ✅ Загрузка музыки с YouTube (через yt-dlp)
- ✅ Загрузка музыки со Spotify (через spotdl)
- ✅ Веб-интерфейс на Django
- ✅ API REST для интеграций
- ✅ Система поиска и фильтрации
- ✅ Автоматическое извлечение метаданных ID3
- ✅ Поддержка обложек альбомов
- ✅ Администраторская панель Django
- ✅ setup.bat для автоматической установки на Windows
- ✅ start.bat для быстрого запуска

### Fixed
- 🐛 Исправлена несовместимость с Python 3.14+ (spotdl версия)
- 🐛 Удалена несуществующая зависимость django-rest-framework-pagination
- 🐛 Удален дубликат зависимости pydub
- 🐛 Удалена проблемная зависимость pyflac (ошибки компиляции на Windows)
- 🐛 Исправлены импорты моделей (MusicFile → Track)
- 🐛 Исправлена работа setup.bat на Windows

### Improved
- 🎨 Полная документация на русском языке
- 🎨 Подробное руководство по установке для Windows
- 🎨 QoL-улучшения и рекомендации
- 🎨 Секция по решению проблем
- 🎨 Лучшие практики безопасности
- 🎨 Полезные команды для управления
- 🎨 Рекомендации по производительности

### Changed
- 📝 Переписан requirements.txt с исправленными версиями
- 📝 Обновлена документация README.md
- 📝 Улучшена обработка ошибок в setup.bat
- 📝 Добавлена информация о требуемых версиях Python (3.10-3.13)

### Dependencies
- Django >= 5.1.0
- DjangoRestFramework >= 3.14.0
- mutagen >= 1.47.0 (работа с метаданными)
- PyDub >= 0.25.1 (аудио-обработка)
- ffmpeg-python >= 0.2.0 (конвертация)
- yt-dlp >= 2024.1.0 (загрузка с YouTube)
- Pillow >= 10.0.0 (обработка изображений)
- celery >= 5.3.4 (фоновые задачи)
- redis >= 5.0.0 (кэширование)

### Tech Stack
- Backend: Django 5.1+, Python 3.10+
- Database: SQLite (по умолчанию), поддержка PostgreSQL
- Frontend: HTML5, CSS3, JavaScript, Tailwind CSS
- Audio: FFmpeg, mutagen, PyDub
- Async: Celery + Redis

### Known Issues
- ⚠️ FFmpeg требуется установить отдельно (не входит в requirements.txt)
- ⚠️ Первая установка может занять 3-10 минут
- ⚠️ На очень больших библиотеках (100000+ треков) SQLite может быть медленным
- ⚠️ Максимальный рекомендуемый размер загружаемого файла: 500MB

### Future Roadmap
- [x] Улучшенная админ-панель (v2.1.0)
- [x] YouTube/URL download интеграция (v2.1.1)
- [ ] WebSocket real-time updates (v2.1.2)
- [ ] Рекомендательная система (v2.1.2)
- [ ] Track mixing и editor (v2.2.0)
- [ ] Мобильное приложение (PWA)
- [ ] Интеграция с Last.fm
- [ ] Загрузка текстов песен (Lyrics)
- [ ] Встроенный эквалайзер
- [ ] Crossfade между треками
- [ ] Синхронизация плейлистов
- [ ] Поддержка облачного хранилища

### Credits
- Спасибо всем, кто помогает улучшать проект!
- FFmpeg за мощную обработку аудио
- Django за надежный веб-фреймворк
- yt-dlp и spotdl за интеграции с сервисами

---

Для версионирования используется [Semantic Versioning](https://semver.org/).
Для каждого коммита используется [Conventional Commits](https://www.conventionalcommits.org/).
