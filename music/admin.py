from django.contrib import admin
from .models import Genre, Artist, Album, Track, Playlist, Favorite, DownloadHistory, ConversionQueue


# Genre Admin
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


# Artist Admin
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('name',)


# Album Admin
@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'year', 'genre', 'created_at')
    list_filter = ('artist', 'genre', 'year')
    search_fields = ('title', 'artist__name')
    ordering = ('-year', 'title')


# Track Admin
@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'format', 'quality', 'duration', 'play_count', 'uploaded_at')
    list_filter = ('artist', 'album', 'genre', 'format', 'quality', 'uploaded_at')
    search_fields = ('title', 'artist__name', 'album__title')
    readonly_fields = ('uploaded_at', 'file_size', 'duration')
    ordering = ('-uploaded_at',)


# Playlist Admin
@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'is_public')
    list_filter = ('is_public', 'created_at')
    search_fields = ('name', 'user__username')
    filter_horizontal = ('tracks',)
    ordering = ('-created_at',)


# Favorite Admin
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username', 'track__title')
    ordering = ('-created_at',)


# DownloadHistory Admin
@admin.register(DownloadHistory)
class DownloadHistoryAdmin(admin.ModelAdmin):
    list_display = ('track', 'user', 'format_downloaded', 'ip_address', 'downloaded_at')
    list_filter = ('format_downloaded', 'downloaded_at')
    search_fields = ('track__title', 'user__username', 'ip_address')
    readonly_fields = ('downloaded_at',)
    ordering = ('-downloaded_at',)


# ConversionQueue Admin
@admin.register(ConversionQueue)
class ConversionQueueAdmin(admin.ModelAdmin):
    list_display = ('track', 'target_format', 'target_quality', 'status', 'created_at', 'completed_at')
    list_filter = ('status', 'target_format', 'created_at')
    search_fields = ('track__title',)
    readonly_fields = ('created_at', 'completed_at')
    ordering = ('-created_at',)
