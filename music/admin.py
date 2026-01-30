from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Sum
from .models import (
    Genre, Artist, Album, MusicFile, Playlist,
    Favorite, SystemSettings, UploadSession
)


# ============================================================================
# Custom Admin Site Configuration
# ============================================================================

class MusicStreamAdminSite(admin.AdminSite):
    site_header = "🎵 Music Stream Admin"
    site_title = "Music Stream Admin Portal"
    index_title = "Welcome to Music Stream Administration"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Load statistics
        settings = SystemSettings.load()
        extra_context['stats'] = {
            'total_tracks': MusicFile.objects.count(),
            'total_artists': Artist.objects.count(),
            'total_albums': Album.objects.count(),
            'total_users': User.objects.count(),
            'total_plays': MusicFile.objects.aggregate(Sum('play_count'))['play_count__sum'] or 0,
            'total_downloads': MusicFile.objects.aggregate(Sum('download_count'))['download_count__sum'] or 0,
            'recent_uploads': UploadSession.objects.filter(status='completed')[:5],
        }

        return super().index(request, extra_context)


# Initialize custom admin site
admin_site = MusicStreamAdminSite(name='music_admin')


# ============================================================================
# Genre Admin
# ============================================================================

@admin.register(Genre, site=admin_site)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'track_count', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at', 'track_count')

    def track_count(self, obj):
        count = obj.musicfile_set.count()
        return format_html(
            '<span style="background: #1db954; color: white; padding: 4px 8px; '
            'border-radius: 12px; font-weight: bold;">{}</span>',
            count
        )
    track_count.short_description = "Tracks"


# ============================================================================
# Artist Admin with Enhanced Stats
# ============================================================================

@admin.register(Artist, site=admin_site)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo_preview', 'track_count', 'total_plays', 'created_at')
    search_fields = ('name', 'bio')
    list_filter = ('created_at',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'photo_preview', 'track_count', 'total_plays')

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'bio', 'website')
        }),
        ('Media', {
            'fields': ('photo', 'photo_preview')
        }),
        ('Statistics', {
            'fields': ('track_count', 'total_plays', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px; '
                'object-fit: cover; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">',
                obj.photo.url
            )
        return "No photo"
    photo_preview.short_description = "Photo Preview"

    def track_count(self, obj):
        return obj.tracks.count()
    track_count.short_description = "Total Tracks"

    def total_plays(self, obj):
        total = obj.tracks.aggregate(Sum('play_count'))['play_count__sum'] or 0
        return format_html('<strong>{:,}</strong>', total)
    total_plays.short_description = "Total Plays"


# ============================================================================
# Album Admin
# ============================================================================

@admin.register(Album, site=admin_site)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'year', 'genre', 'cover_preview', 'track_count', 'created_at')
    list_filter = ('artist', 'genre', 'year', 'created_at')
    search_fields = ('title', 'artist__name')
    ordering = ('-year', 'title')
    readonly_fields = ('created_at', 'cover_preview', 'track_count')
    autocomplete_fields = ['artist']

    def cover_preview(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" style="width: 80px; height: 80px; '
                'object-fit: cover; border-radius: 8px;">',
                obj.cover.url
            )
        return "No cover"
    cover_preview.short_description = "Cover"

    def track_count(self, obj):
        return obj.tracks.count()
    track_count.short_description = "Tracks"


# ============================================================================
# Enhanced MusicFile Admin
# ============================================================================

@admin.register(MusicFile, site=admin_site)
class MusicFileAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'artist', 'album', 'format_badge',
        'duration_display', 'play_count_badge', 'audio_preview'
    )
    list_filter = ('artist', 'album', 'genre', 'format', 'created_at')
    search_fields = ('title', 'artist__name', 'album__title')
    readonly_fields = (
        'created_at', 'updated_at', 'file_size_display',
        'duration', 'play_count', 'download_count', 'audio_player'
    )
    ordering = ('-created_at',)
    autocomplete_fields = ['artist', 'album', 'genre']

    fieldsets = (
        ('Track Info', {
            'fields': ('title', 'artist', 'album', 'genre')
        }),
        ('File', {
            'fields': ('file', 'format', 'file_size_display')
        }),
        ('Metadata', {
            'fields': ('duration', 'bitrate'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('play_count', 'download_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Preview', {
            'fields': ('audio_player',)
        }),
    )

    actions = ['reset_play_count', 'extract_metadata']

    def format_badge(self, obj):
        colors = {
            'mp3': '#FF6B6B',
            'flac': '#4ECDC4',
            'wav': '#45B7D1',
            'm4a': '#FFA07A',
            'ogg': '#98D8C8',
        }
        color = colors.get(obj.format, '#999')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.format.upper()
        )
    format_badge.short_description = "Format"

    def duration_display(self, obj):
        minutes, seconds = divmod(obj.duration, 60)
        return f"{minutes}:{seconds:02d}"
    duration_display.short_description = "Duration"

    def play_count_badge(self, obj):
        if obj.play_count > 1000:
            return format_html(
                '<span style="background: #1db954; color: white; padding: 4px 10px; '
                'border-radius: 12px; font-weight: bold;">🔥 {:,}</span>',
                obj.play_count
            )
        return format_html('<strong>{:,}</strong>', obj.play_count)
    play_count_badge.short_description = "Plays"

    def audio_preview(self, obj):
        if obj.file:
            return format_html(
                '<audio controls preload="none" style="width: 200px; height: 32px;">'
                '<source src="{}" type="audio/{}"></audio>',
                obj.file.url, obj.format
            )
        return "—"
    audio_preview.short_description = "Quick Preview"

    def audio_player(self, obj):
        if obj.file:
            return format_html(
                '<div style="background: #f8f9fa; padding: 20px; border-radius: 12px;">'
                '<audio controls style="width: 100%;">'
                '<source src="{}" type="audio/{}"></audio>'
                '<div style="margin-top: 12px; color: #666; font-size: 13px;">'
                'File: <strong>{}</strong> | Size: <strong>{}</strong> | Bitrate: <strong>{} kbps</strong>'
                '</div></div>',
                obj.file.url, obj.format, obj.file.name,
                f"{obj.file_size / (1024**2):.2f} MB",
                obj.bitrate or "N/A"
            )
        return "No file"
    audio_player.short_description = "Audio Player"

    def file_size_display(self, obj):
        size_mb = obj.file_size / (1024 ** 2)
        return f"{size_mb:.2f} MB"
    file_size_display.short_description = "File Size"

    def reset_play_count(self, request, queryset):
        updated = queryset.update(play_count=0)
        self.message_user(request, f"{updated} tracks reset.")
    reset_play_count.short_description = "Reset play count"

    def extract_metadata(self, request, queryset):
        for track in queryset:
            track.save()  # Triggers metadata extraction
        self.message_user(request, f"Metadata extracted for {queryset.count()} tracks.")
    extract_metadata.short_description = "Re-extract metadata"


# ============================================================================
# System Settings Admin
# ============================================================================

@admin.register(SystemSettings, site=admin_site)
class SystemSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General Settings', {
            'fields': ('site_name', 'site_description', 'max_upload_size', 'allowed_formats')
        }),
        ('User Management', {
            'fields': ('allow_registration', 'require_email_verification', 'max_uploads_per_user')
        }),
        ('Audio Processing', {
            'fields': ('auto_extract_metadata', 'auto_generate_waveforms', 'normalize_audio')
        }),
        ('UI Settings', {
            'fields': ('default_theme', 'enable_animations')
        }),
        ('Statistics (Read-only)', {
            'fields': ('total_tracks', 'total_plays', 'total_downloads', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('total_tracks', 'total_plays', 'total_downloads', 'created_at', 'updated_at')

    def has_add_permission(self, request):
        # Only one instance allowed (singleton)
        return not SystemSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ============================================================================
# Upload Session Admin
# ============================================================================

@admin.register(UploadSession, site=admin_site)
class UploadSessionAdmin(admin.ModelAdmin):
    list_display = ('id_short', 'user', 'status_badge', 'progress', 'created_at', 'duration')
    list_filter = ('status', 'user', 'created_at')
    search_fields = ('user__username', 'id')
    readonly_fields = ('id', 'user', 'total_files', 'successful_uploads', 'failed_uploads',
                       'status', 'error_log', 'created_at', 'completed_at')
    ordering = ('-created_at',)

    def id_short(self, obj):
        return str(obj.id)[:8]
    id_short.short_description = "Session ID"

    def status_badge(self, obj):
        colors = {
            'pending': '#FFA500',
            'processing': '#4ECDC4',
            'completed': '#1db954',
            'failed': '#FF6B6B',
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 10px; '
            'border-radius: 12px; font-weight: bold;">{}</span>',
            color, obj.status.upper()
        )
    status_badge.short_description = "Status"

    def progress(self, obj):
        if obj.total_files == 0:
            return "—"
        percent = (obj.successful_uploads / obj.total_files) * 100
        return format_html(
            '<div style="background: #e0e0e0; border-radius: 10px; width: 100px; height: 20px;">'
            '<div style="background: #1db954; width: {}%; height: 100%; border-radius: 10px;"></div>'
            '</div><small>{}/{}</small>',
            percent, obj.successful_uploads, obj.total_files
        )
    progress.short_description = "Progress"

    def duration(self, obj):
        if obj.completed_at:
            delta = obj.completed_at - obj.created_at
            return f"{delta.total_seconds():.1f}s"
        return "—"
    duration.short_description = "Duration"


# ============================================================================
# Playlist & Favorite Admin
# ============================================================================

@admin.register(Playlist, site=admin_site)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'track_count', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at', 'user')
    search_fields = ('name', 'user__username')
    filter_horizontal = ('tracks',)
    ordering = ('-created_at',)

    def track_count(self, obj):
        return obj.tracks.count()
    track_count.short_description = "Tracks"


@admin.register(Favorite, site=admin_site)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username', 'track__title')
    ordering = ('-created_at',)
