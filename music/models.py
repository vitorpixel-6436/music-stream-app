import uuid
import os
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Genre(models.Model):
    """Music genre model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Artist(models.Model):
    """Artist model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
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
    """Album model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    year = models.IntegerField(null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-year', 'title']
        unique_together = ['title', 'artist']
    
    def __str__(self):
        return f"{self.title} - {self.artist.name}"


class MusicFile(models.Model):
    """Enhanced music file model with FLAC support and quality options"""
    
    FORMAT_CHOICES = [
        ('mp3', 'MP3'),
        ('flac', 'FLAC'),
        ('ogg', 'OGG'),
        ('m4a', 'M4A'),
        ('wav', 'WAV'),
    ]
    
    QUALITY_CHOICES = [
        ('low', '128kbps'),
        ('medium', '192kbps'),
        ('high', '320kbps'),
        ('lossless', 'Lossless (FLAC)'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='tracks')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='tracks')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    
    # File fields for different formats
    file = models.FileField(
        upload_to='tracks/',
        validators=[FileExtensionValidator(['mp3', 'flac', 'ogg', 'm4a', 'wav'])]
    )
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='mp3')
    quality = models.CharField(max_length=20, choices=QUALITY_CHOICES, default='high')
    
    # Metadata
    duration = models.IntegerField(default=0, help_text="Duration in seconds")
    bitrate = models.IntegerField(null=True, blank=True, help_text="Bitrate in kbps")
    sample_rate = models.IntegerField(null=True, blank=True, help_text="Sample rate in Hz")
    file_size = models.BigIntegerField(default=0, help_text="File size in bytes")
    
    # Additional info
    year = models.IntegerField(null=True, blank=True)
    track_number = models.IntegerField(null=True, blank=True)
    lyrics = models.TextField(blank=True)
    
    # Statistics
    play_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)
    
    # External source info
    source_url = models.URLField(blank=True, help_text="URL where track was downloaded from")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['artist', 'title']),
            models.Index(fields=['genre']),
            models.Index(fields=['format']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.artist.name} ({self.format.upper()})"
    
    def get_file_extension(self):
        return os.path.splitext(self.file.name)[1][1:]
    
    def increment_play_count(self):
        self.play_count += 1
        self.save(update_fields=['play_count'])
    
    def increment_download_count(self):
        self.download_count += 1
        self.save(update_fields=['download_count'])


class Playlist(models.Model):
    """User playlist model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    tracks = models.ManyToManyField(MusicFile, related_name='playlists', blank=True)
    cover = models.ImageField(upload_to='playlist_covers/', blank=True, null=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.name} by {self.user.username}"
    
    def track_count(self):
        return self.tracks.count()


class Favorite(models.Model):
    """User favorites model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    track = models.ForeignKey(MusicFile, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'track']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.track.title}"


class DownloadHistory(models.Model):
    """Track download history"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    track = models.ForeignKey(MusicFile, on_delete=models.CASCADE)
    format_downloaded = models.CharField(max_length=10)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-downloaded_at']
    
    def __str__(self):
        return f"{self.track.title} - {self.downloaded_at}"


class ConversionQueue(models.Model):
    """Queue for format conversion tasks"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    track = models.ForeignKey(MusicFile, on_delete=models.CASCADE)
    target_format = models.CharField(max_length=10)
    target_quality = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result_file = models.FileField(upload_to='converted/', blank=True, null=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.track.title} -> {self.target_format} ({self.status})"
