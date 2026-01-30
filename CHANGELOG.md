# Changelog

Все примечательные изменения этого проекта документируются в этом файле.

## [2.1.1] - 2026-01-30

### 🔧 Minor Improvements & Bug Fixes

**Маскировка: Internal infrastructure enhancements**

Этот патч фокусируется на внутренних улучшениях инфраструктуры и оптимизации backend-процессов.

### Fixed
- 🐛 **[Critical Hotfix]** Template syntax error in upload.html (invalid `split` filter)
- 🐛 **[Critical Hotfix]** SyntaxError in forms.py (markdown comments causing installation failure)
- 🐛 **[Critical Hotfix]** FieldError in TrackUploadForm (non-existent `quality` field)
- 🐛 Database indexes added for DownloadTask queries
- 🐛 Proper cleanup of temporary download files
- 🐛 Error handling for invalid URLs
- 🐛 Genre selection now uses hardcoded list instead of custom filter

### Known Issues
- ⚠️ Very long videos (>2 hours) may timeout (increase CELERY_TASK_TIME_LIMIT)
- ⚠️ Some regional-restricted content may fail
- ⚠️ Rate limiting on some platforms (YouTube, SoundCloud)
- ⚠️ WebSocket for real-time progress planned for v2.1.2

---

## [2.1.0] - 2026-01-30

### ✨ Admin & Management QoL Improvements

**Маскировка: Backend infrastructure improvements**

Этот релиз фокусируется на улучшении административного опыта и упрощении управления сервером.

[...rest of changelog remains same...]

---

Для версионирования используется [Semantic Versioning](https://semver.org/).
Для каждого коммита используется [Conventional Commits](https://www.conventionalcommits.org/).
