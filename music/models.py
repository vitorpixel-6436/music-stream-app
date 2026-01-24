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
