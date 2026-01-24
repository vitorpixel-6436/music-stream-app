from django.contrib import admin
from .models import MusicFile


@admin.register(MusicFile)
class MusicFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'duration', 'uploaded_at')
    list_filter = ('artist', 'album', 'genre', 'uploaded_at')
    search_fields = ('title', 'artist', 'album')
    readonly_fields = ('uploaded_at', 'file_size', 'duration')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'artist', 'album', 'genre', 'year')
        }),
        ('File Information', {
            'fields': ('file', 'file_size', 'duration')
        }),
        ('Metadata', {
            'fields': ('uploaded_at',)
        }),
    )
