import uuid
import os
import logging
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from mutagen import File as MutagenFile

logger = logging.getLogger(__name__)

class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Artist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='artists/', blank=True, null=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Album(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    year = models.IntegerField(null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', 'title']
        unique_together = ['title', 'artist']

    def __str__(self):
        return f"{self.title} - {self.artist.name}"

class MusicFile(models.Model):
    FORMAT_CHOICES = [
        ('mp3', 'MP3'),
        ('flac', 'FLAC'),
        ('ogg', 'OGG'),
        ('m4a', 'M4A'),
        ('wav', 'WAV'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='tracks')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='tracks')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(
        upload_to='tracks/',
        validators=[FileExtensionValidator(['mp3', 'flac', 'ogg', 'm4a', 'wav'])]
    )
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='mp3')
    
    # Metadata (Auto-extracted)
    duration = models.IntegerField(default=0, help_text="Duration in seconds")
    file_size = models.BigIntegerField(default=0)
    bitrate = models.IntegerField(null=True, blank=True)
    
    # Statistics
    play_count = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['artist', 'title']),
        ]

    def __str__(self):
        return f"{self.title} - {self.artist.name}"

    def save(self, *args, **kwargs):
        if self.file and not self.duration:
            try:
                self.file_size = self.file.size
                audio = MutagenFile(self.file)
                if audio and audio.info:
                    self.duration = int(audio.info.length)
                    if hasattr(audio.info, 'bitrate'):
                        self.bitrate = int(audio.info.bitrate / 1000)
            except Exception as e:
                logger.error(f"Metadata extraction error: {e}")
        
        # Ensure format is lowercase extension
        if self.file and not self.format:
            self.format = os.path.splitext(self.file.name)[1][1:].lower()
            
        super().save(*args, **kwargs)

    def increment_play_count(self):
        self.play_count += 1
        self.save(update_fields=['play_count'])

    def increment_download_count(self):
        self.download_count += 1
        self.save(update_fields=['download_count'])

class Playlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    tracks = models.ManyToManyField(MusicFile, related_name='playlists', blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.user.username}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(MusicFile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'track']


# ============================================================================
# v2.1.0: Admin & Management QoL Features
# ============================================================================

class SystemSettings(models.Model):
    """Singleton модель для системных настроек"""
    
    # General Settings
    site_name = models.CharField(max_length=100, default="Music Stream App")
    site_description = models.TextField(blank=True, default="Premium music streaming application")
    max_upload_size = models.IntegerField(default=100, help_text="Max upload size in MB")
    allowed_formats = models.CharField(
        max_length=255, 
        default="mp3,flac,wav,m4a,ogg",
        help_text="Comma-separated list of allowed audio formats"
    )
    
    # User Management
    allow_registration = models.BooleanField(default=True)
    require_email_verification = models.BooleanField(default=False)
    max_uploads_per_user = models.IntegerField(default=100, help_text="0 = unlimited")
    
    # Audio Processing
    auto_extract_metadata = models.BooleanField(default=True)
    auto_generate_waveforms = models.BooleanField(default=False)
    normalize_audio = models.BooleanField(default=False)
    
    # UI Settings
    default_theme = models.CharField(
        max_length=20,
        choices=[
            ('glass', 'Apple Glass'),
            ('steam', 'Steam Gaming'),
            ('spotify', 'Spotify Minimal'),
            ('msi', 'MSI Gaming'),
        ],
        default='glass'
    )
    enable_animations = models.BooleanField(default=True)
    
    # Statistics
    total_tracks = models.PositiveIntegerField(default=0, editable=False)
    total_plays = models.PositiveIntegerField(default=0, editable=False)
    total_downloads = models.PositiveIntegerField(default=0, editable=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "System Settings"
        verbose_name_plural = "System Settings"
    
    def save(self, *args, **kwargs):
        # Singleton pattern - only one instance allowed
        self.pk = 1
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Prevent deletion
        pass
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    def __str__(self):
        return f"Settings - {self.site_name}"
    
    def update_statistics(self):
        """Update cached statistics"""
        self.total_tracks = MusicFile.objects.count()
        self.total_plays = MusicFile.objects.aggregate(
            total=models.Sum('play_count')
        )['total'] or 0
        self.total_downloads = MusicFile.objects.aggregate(
            total=models.Sum('download_count')
        )['total'] or 0
        self.save(update_fields=['total_tracks', 'total_plays', 'total_downloads'])


class UploadSession(models.Model):
    """Track bulk upload sessions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upload_sessions')
    total_files = models.PositiveIntegerField(default=0)
    successful_uploads = models.PositiveIntegerField(default=0)
    failed_uploads = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    error_log = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Upload Session {self.id} - {self.user.username}"
