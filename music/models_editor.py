"""Audio Editor Models - Foundation for non-destructive audio mixing and editing.

Supports multi-layer mixing with pydub backend, flexible config-based architecture
for easy extension to effects, automation, and advanced features.
"""

import uuid
from django.db import models
from django.contrib.auth.models import User
from .models import MusicFile


class AudioEditProject(models.Model):
    """
    Audio editing project that stores configuration for mixing multiple tracks.
    
    Non-destructive: stores only config, original files untouched.
    Supports multiple layers with offsets, gains, fades, and future effects.
    """
    
    # Metadata
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='audio_edit_projects'
    )
    name = models.CharField(
        max_length=255,
        help_text='Project name (e.g., "DJ Mix v2")'
    )
    description = models.TextField(
        blank=True,
        default='',
        help_text='Project description'
    )
    
    # Base track (primary track to mix into)
    base_track = models.ForeignKey(
        MusicFile,
        on_delete=models.CASCADE,
        related_name='edit_projects_base'
    )
    
    # Result (generated mix)
    result_track = models.ForeignKey(
        MusicFile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='edit_results',
        help_text='Generated mix file (auto-created after export)'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Editor config (JSON)
    # Structure:
    # {
    #   "layers": [
    #     {
    #       "track_id": "<uuid>",
    #       "offset_ms": 30000,
    #       "gain_db": -3.0,
    #       "fade_in_ms": 2000,
    #       "fade_out_ms": 3000,
    #       "enabled": true
    #     },
    #     ...
    #   ],
    #   "master_gain_db": 0.0,
    #   "metadata": {
    #     "bpm": 120,
    #     "key": "C",
    #     "notes": "DJ transition mix"
    #   }
    # }
    config = models.JSONField(
        default=dict,
        help_text='Editor configuration: layers, effects, automation'
    )
    
    # Preview file (temporary, regenerated on changes)
    preview_file = models.FileField(
        upload_to='editor/previews/',
        null=True,
        blank=True,
        help_text='Cached preview file'
    )
    
    class Meta:
        db_table = 'music_audio_edit_project'
        indexes = [
            models.Index(fields=['user', '-updated_at']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'Audio Edit Project'
        verbose_name_plural = 'Audio Edit Projects'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
    def get_config(self):
        """Get config with defaults."""
        return self.config or {"layers": [], "master_gain_db": 0.0}
    
    def get_layers(self):
        """Get all enabled layers."""
        return [
            layer for layer in self.get_config().get("layers", [])
            if layer.get("enabled", True)
        ]
    
    def add_layer(self, track_id: str, offset_ms: int = 0,
                  gain_db: float = 0.0, fade_in_ms: int = 0,
                  fade_out_ms: int = 0):
        """Add a new mixing layer."""
        config = self.get_config()
        if "layers" not in config:
            config["layers"] = []
        
        config["layers"].append({
            "track_id": str(track_id),
            "offset_ms": offset_ms,
            "gain_db": gain_db,
            "fade_in_ms": fade_in_ms,
            "fade_out_ms": fade_out_ms,
            "enabled": True
        })
        
        self.config = config
        return self
    
    def set_master_gain(self, gain_db: float):
        """Set master output gain in dB."""
        config = self.get_config()
        config["master_gain_db"] = gain_db
        self.config = config
        return self
