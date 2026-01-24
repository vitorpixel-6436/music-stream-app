from django.contrib import admin
from .models import Genre, Artist, Album, MusicFile, Playlist, Favorite
from django.utils.html import format_html

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

# MusicFile Admin
@admin.register(MusicFile)
class MusicFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'format', 'duration', 'play_count', 'created_at', 'preview')
    list_filter = ('artist', 'album', 'genre', 'format', 'created_at')
    search_fields = ('title', 'artist__name', 'album__title')
    readonly_fields = ('created_at', 'updated_at', 'file_size', 'duration', 'play_count', 'download_count')
    ordering = ('-created_at',)
    
    def preview(self, obj):
        if obj.file:
            return format_html(
                '<audio controls style="width: 200px;"'
                '<source src="{}" type="audio/mpeg">'
                'Your browser does not support audio.'
                '</audio>',
                obj.file.url
            )
        return "-"
    preview.short_description = "Audio Preview"

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
