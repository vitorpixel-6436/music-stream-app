"""Audio Editor Engine - pydub-based audio mixing and rendering.

Handles multi-layer mixing, gain adjustments, fades, and preview/export.
Supports non-destructive editing through config-based project structure.
"""

import logging
import os
from pathlib import Path
from typing import Optional, BinaryIO

from pydub import AudioSegment
from django.conf import settings
from django.core.files.base import ContentFile

from .models import MusicFile

logger = logging.getLogger(__name__)

# Pydub format mapping
FORMAT_MAP = {
    'mp3': 'mp3',
    'wav': 'wav',
    'flac': 'flac',
    'ogg': 'ogg',
    'm4a': 'm4a',
}


class AudioEditorEngine:
    """
    Non-destructive audio editor using pydub.
    
    Renders projects to temporary/permanent files without modifying originals.
    """
    
    def __init__(self, project):
        """
        Args:
            project: AudioEditProject instance
        """
        self.project = project
        self.base_track = project.base_track
        self.config = project.get_config()
        self.logger = logger
    
    def render_preview(self, export_format: str = 'mp3') -> str:
        """
        Render project to temporary preview file.
        
        Args:
            export_format: 'mp3', 'wav', 'flac', etc
        
        Returns:
            Path to preview file
        """
        self.logger.info(f'Rendering preview for project {self.project.id}')
        
        try:
            # Load and mix tracks
            mix = self._mix_tracks()
            
            # Create temp directory
            temp_dir = Path(settings.MEDIA_ROOT) / 'editor' / 'temp'
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            # Export to temp file
            temp_path = temp_dir / f'{self.project.id}_preview.{export_format}'
            mix.export(
                str(temp_path),
                format=export_format,
                bitrate='192k',  # Preview quality
                parameters=['-q:a', '4']  # ffmpeg quality
            )
            
            self.logger.info(f'Preview rendered: {temp_path}')
            return str(temp_path)
        
        except Exception as e:
            self.logger.error(f'Preview render failed: {e}')
            raise
    
    def render_final(self, export_format: str = 'flac',
                     export_bitrate: str = '320k') -> MusicFile:
        """
        Render project to final MusicFile (high quality).
        
        Args:
            export_format: 'flac', 'mp3', etc
            export_bitrate: Bitrate for MP3 export
        
        Returns:
            Created MusicFile instance
        """
        self.logger.info(f'Rendering final export for project {self.project.id}')
        
        try:
            # Load and mix tracks
            mix = self._mix_tracks()
            
            # Create output directory
            output_dir = Path(settings.MEDIA_ROOT) / 'editor' / 'exports'
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Export to file
            output_path = output_dir / f'{self.project.id}_mix.{export_format}'
            
            if export_format.lower() == 'mp3':
                mix.export(
                    str(output_path),
                    format='mp3',
                    bitrate=export_bitrate,
                    parameters=['-q:a', '2']  # High quality
                )
            else:
                mix.export(
                    str(output_path),
                    format=export_format
                )
            
            # Create MusicFile instance
            music_file = self._create_musicfile_from_path(
                output_path,
                self.project
            )
            
            # Update project
            self.project.result_track = music_file
            self.project.save(update_fields=['result_track'])
            
            self.logger.info(f'Final export created: {music_file.id}')
            return music_file
        
        except Exception as e:
            self.logger.error(f'Final export failed: {e}')
            raise
    
    def _mix_tracks(self) -> AudioSegment:
        """
        Mix all enabled layers with base track.
        
        Returns:
            Mixed AudioSegment
        """
        # Load base track
        base = self._load_segment(self.base_track)
        
        # Apply master gain to base
        master_gain = self.config.get('master_gain_db', 0.0)
        if master_gain != 0.0:
            base = base + master_gain
        
        # Overlay each layer
        for layer in self.project.get_layers():
            try:
                track = MusicFile.objects.get(id=layer['track_id'])
                segment = self._load_segment(track)
                
                # Apply layer gain
                layer_gain = layer.get('gain_db', 0.0)
                if layer_gain != 0.0:
                    segment = segment + layer_gain
                
                # Apply fades
                fade_in = layer.get('fade_in_ms', 0)
                fade_out = layer.get('fade_out_ms', 0)
                if fade_in > 0:
                    segment = segment.fade_in(fade_in)
                if fade_out > 0:
                    segment = segment.fade_out(fade_out)
                
                # Overlay at offset
                offset = layer.get('offset_ms', 0)
                base = base.overlay(segment, position=offset)
                
                self.logger.debug(f'Layer {layer["track_id"]} mixed at +{offset}ms')
            
            except MusicFile.DoesNotExist:
                self.logger.warning(f'Track {layer["track_id"]} not found, skipping')
            except Exception as e:
                self.logger.error(f'Failed to mix layer: {e}')
                raise
        
        return base
    
    def _load_segment(self, track: MusicFile) -> AudioSegment:
        """
        Load MusicFile as AudioSegment.
        
        Args:
            track: MusicFile instance
        
        Returns:
            AudioSegment
        """
        if not track.file or not os.path.exists(track.file.path):
            raise FileNotFoundError(f'Track file not found: {track.id}')
        
        # Detect format
        file_ext = Path(track.file.path).suffix.lstrip('.').lower()
        fmt = FORMAT_MAP.get(file_ext, file_ext)
        
        try:
            return AudioSegment.from_file(
                track.file.path,
                format=fmt
            )
        except Exception as e:
            self.logger.error(f'Failed to load track {track.id}: {e}')
            raise
    
    def _create_musicfile_from_path(self, file_path: Path,
                                     project) -> MusicFile:
        """
        Create MusicFile from rendered audio path.
        
        Args:
            file_path: Path to audio file
            project: AudioEditProject instance
        
        Returns:
            Created MusicFile
        """
        base = self.base_track
        
        # Create title
        title = f'{project.name} [Mix]'
        
        # Open file and create MusicFile
        with open(file_path, 'rb') as f:
            content = ContentFile(f.read(), name=file_path.name)
            
            music_file = MusicFile(
                title=title,
                artist=base.artist or 'Various',
                album=base.album or project.name,
                genre=base.genre or 'Mix',
                format=file_path.suffix.lstrip('.').lower(),
                file=content
            )
            music_file.save()
        
        self.logger.info(f'MusicFile created: {music_file.id}')
        return music_file


def render_project_preview(project_id: str, fmt: str = 'mp3') -> str:
    """Convenience function for preview rendering."""
    from .models_editor import AudioEditProject
    project = AudioEditProject.objects.get(id=project_id)
    engine = AudioEditorEngine(project)
    return engine.render_preview(fmt)


def render_project_final(project_id: str, fmt: str = 'flac') -> MusicFile:
    """Convenience function for final export."""
    from .models_editor import AudioEditProject
    project = AudioEditProject.objects.get(id=project_id)
    engine = AudioEditorEngine(project)
    return engine.render_final(fmt)
