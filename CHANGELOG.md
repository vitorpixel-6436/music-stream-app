# Changelog

Все примечательные изменения этого проекта документируются в этом файле.

## [2.1.1] - 2026-01-30

### 🔧 Minor Improvements & Bug Fixes

**Маскировка: Internal infrastructure enhancements**

Этот патч фокусируется на внутренних улучшениях инфраструктуры и оптимизации backend-процессов.

#### Added
- ✅ **DownloadTask Model** - Background task tracking system
- ✅ **Download Manager Views** - Web interface for task monitoring
- ✅ **Media Downloader Utility** - Helper for external content
- ✅ **Celery Background Tasks** - Async processing
- ✅ **Admin Panel Integration** - Download task management
- ✅ **URLImportForm** - Form for importing music from YouTube, SoundCloud, Bandcamp

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
- 🐛 **[Critical Hotfix]** Template syntax error in upload.html (invalid `split` filter)
- 🐛 **[Critical Hotfix]** SyntaxError in forms.py (markdown comments causing installation failure)
- 🐛 **[Critical Hotfix]** FieldError in TrackUploadForm (non-existent `quality` field removed)
- 🐛 **[Critical Hotfix]** FieldError in PlaylistCreateForm (non-existent `description` field removed)
- 🐛 **[Critical Hotfix]** NodeNotFoundError in migrations (0003_download_task dependency fixed)
- 🐛 Database indexes added for DownloadTask queries
- 🐛 Proper cleanup of temporary download files
- 🐛 Error handling for invalid URLs
- 🐛 Genre selection now uses hardcoded list instead of custom filter

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
- ✅ **SystemSettings Model** - Singleton model for system-wide settings
- ✅ **UploadSession Model** - Track bulk upload sessions
- ✅ **Management Commands** - CLI tools for administration
- ✅ **Enhanced Admin Panel** - Rich UI with widgets and statistics

### Improved
- 🎨 Admin UI with color-coded badges and previews
- 🎨 Simplified user management via CLI
- 🎨 Centralized settings through admin panel
- 🎨 Visual progress for batch operations

### Changed
- 📝 Admin site renamed to MusicStreamAdminSite
- 📝 Added readonly fields for metadata
- 📝 Improved fieldsets structure in all admin classes

### Future Enhancements (v2.1.1+)
- [x] URL download integration (v2.1.1 ✅)
- [ ] WebUI for SystemSettings (without admin panel)
- [ ] Bulk upload form with drag-and-drop
- [ ] Real-time progress via WebSocket
- [ ] Email notifications for admins
- [ ] Backup/restore functions

---

## [2.0.0] - 2026-01-29

### 🎨 UI Redesign - Four Design Systems

**Premium music streaming application** with four UI design systems:

#### Added
- ✅ **Apple Glass Effects** (37.1 KB)
- ✅ **Steam Gaming Cards** (35.2 KB)
- ✅ **Spotify Minimalism** (23.0 KB)
- ✅ **MSI Gaming Vibes** (13.0 KB)

#### Stats
- 📊 Total UI Components: **108.3 KB** (4 systems, 12 files)
- 📊 Minified: **~35 KB**
- 📊 Gzipped: **~12 KB**

---

## [1.0.0] - 2026-01-24

### Added
- ✅ Full FLAC and audio format support (MP3, WAV, AAC, OGG)
- ✅ Genre, artist, and album management system
- ✅ Playlist creation and management
- ✅ Favorite tracks system
- ✅ Play and download history
- ✅ Format conversion support (via ffmpeg)
- ✅ YouTube music download (via yt-dlp)
- ✅ Spotify music download (via spotdl)
- ✅ Django web interface
- ✅ REST API for integrations
- ✅ Search and filtering system
- ✅ Automatic ID3 metadata extraction
- ✅ Album cover support
- ✅ Django admin panel
- ✅ setup.bat for automatic Windows installation
- ✅ start.bat for quick launch

### Fixed
- 🐛 Python 3.14+ compatibility (spotdl version)
- 🐛 Removed non-existent django-rest-framework-pagination dependency
- 🐛 Removed pydub duplicate dependency
- 🐛 Removed problematic pyflac dependency (Windows compilation errors)
- 🐛 Fixed model imports (MusicFile → Track)
- 🐛 Fixed setup.bat on Windows

### Improved
- 🎨 Full Russian documentation
- 🎨 Detailed Windows installation guide
- 🎨 QoL improvements and recommendations
- 🎨 Troubleshooting section
- 🎨 Security best practices
- 🎨 Useful management commands
- 🎨 Performance recommendations

### Changed
- 📝 Rewritten requirements.txt with fixed versions
- 📝 Updated README.md documentation
- 📝 Improved error handling in setup.bat
- 📝 Added Python version requirements (3.10-3.13)

### Dependencies
- Django >= 5.1.0
- DjangoRestFramework >= 3.14.0
- mutagen >= 1.47.0 (metadata handling)
- PyDub >= 0.25.1 (audio processing)
- ffmpeg-python >= 0.2.0 (conversion)
- yt-dlp >= 2024.1.0 (YouTube download)
- Pillow >= 10.0.0 (image processing)
- celery >= 5.3.4 (background tasks)
- redis >= 5.0.0 (caching)

### Tech Stack
- Backend: Django 5.1+, Python 3.10+
- Database: SQLite (default), PostgreSQL support
- Frontend: HTML5, CSS3, JavaScript, Tailwind CSS
- Audio: FFmpeg, mutagen, PyDub
- Async: Celery + Redis

### Known Issues
- ⚠️ FFmpeg must be installed separately (not in requirements.txt)
- ⚠️ First installation may take 3-10 minutes
- ⚠️ Very large libraries (100000+ tracks) may be slow with SQLite
- ⚠️ Maximum recommended upload file size: 500MB

### Future Roadmap
- [x] Enhanced admin panel (v2.1.0)
- [x] YouTube/URL download integration (v2.1.1)
- [ ] WebSocket real-time updates (v2.1.2)
- [ ] Recommendation system (v2.1.2)
- [ ] Track mixing and editor (v2.2.0)
- [ ] Mobile app (PWA)
- [ ] Last.fm integration
- [ ] Lyrics download
- [ ] Built-in equalizer
- [ ] Track crossfade
- [ ] Playlist sync
- [ ] Cloud storage support

### Credits
- Thanks to everyone helping improve the project!
- FFmpeg for powerful audio processing
- Django for reliable web framework
- yt-dlp and spotdl for service integrations

---

Для версионирования используется [Semantic Versioning](https://semver.org/).
Для каждого коммита используется [Conventional Commits](https://www.conventionalcommits.org/).
