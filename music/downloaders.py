"""
Media Downloaders
=================

Downloader implementations for various media sources.
Supports YouTube, SoundCloud, Bandcamp, and direct URLs.

Features:
- Progress tracking with callbacks
- Automatic metadata extraction
- Format conversion
- Error handling and retries
"""

import os
import logging
import subprocess
from abc import ABC, abstractmethod
from typing import Dict, Optional, Callable
from django.conf import settings
from django.core.files import File
from .models import DownloadTask, MusicFile, Artist

logger = logging.getLogger(__name__)


class DownloadError(Exception):
    """Custom exception for download errors"""
    pass


class BaseDownloader(ABC):
    """
    Abstract base class for all downloaders.
    
    Subclasses must implement:
    - download()
    - extract_metadata()
    """
    
    def __init__(self, task: DownloadTask, progress_callback: Optional[Callable] = None):
        self.task = task
        self.progress_callback = progress_callback
        self.temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp', 'downloads')
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def update_progress(self, progress: int, step: str = None):
        """Update task progress and call callback if provided"""
        self.task.update_progress(progress, step)
        
        if self.progress_callback:
            self.progress_callback(progress, step)
    
    @abstractmethod
    def download(self) -> str:
        """Download media and return path to downloaded file"""
        pass
    
    @abstractmethod
    def extract_metadata(self, file_path: str) -> Dict[str, any]:
        """Extract metadata from downloaded file"""
        pass
    
    def cleanup(self, file_path: str):
        """Remove temporary files"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up temp file: {file_path}")
        except Exception as e:
            logger.warning(f"Cleanup failed for {file_path}: {e}")


class YouTubeDownloader(BaseDownloader):
    """
    Downloader for YouTube, SoundCloud, Bandcamp using yt-dlp.
    
    Supports:
    - YouTube videos
    - SoundCloud tracks
    - Bandcamp albums/tracks
    - Direct audio URLs
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_template = os.path.join(
            self.temp_dir,
            f"{self.task.id}_%(title)s.%(ext)s"
        )
    
    def _get_yt_dlp_options(self) -> Dict:
        """Build yt-dlp options based on task settings"""
        
        format_mapping = {
            'mp3': 'bestaudio/best',
            'flac': 'bestaudio/best',
            'ogg': 'bestaudio/best',
            'wav': 'bestaudio/best',
            'm4a': 'bestaudio[ext=m4a]/bestaudio/best',
        }
        
        audio_format = self.task.output_format
        audio_quality = self.task.output_quality.replace('k', '')  # '320k' -> '320'
        
        options = {
            'format': format_mapping.get(audio_format, 'bestaudio/best'),
            'outtmpl': self.output_template,
            'quiet': False,
            'no_warnings': False,
            'extractaudio': True,
            'audioformat': audio_format,
            'audioquality': audio_quality,
            
            # Post-processing
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': audio_quality,
            }],
            
            # Progress hooks
            'progress_hooks': [self._progress_hook],
            
            # Metadata
            'writethumbnail': True,
            'embedthumbnail': audio_format in ['mp3', 'm4a'],
            'addmetadata': True,
            
            # Network settings
            'socket_timeout': 30,
            'retries': 3,
            'fragment_retries': 5,
            
            # Prefer free formats
            'prefer_free_formats': True,
        }
        
        return options
    
    def _progress_hook(self, d: Dict):
        """yt-dlp progress callback"""
        try:
            status = d.get('status')
            
            if status == 'downloading':
                # Calculate progress percentage
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                
                if total > 0:
                    progress = int((downloaded / total) * 80)  # 0-80% for download
                    speed = d.get('speed', 0)
                    eta = d.get('eta', 0)
                    
                    step = f"Downloading... {self._format_bytes(downloaded)}/{self._format_bytes(total)}"
                    if speed:
                        step += f" ({self._format_bytes(speed)}/s)"
                    
                    self.update_progress(progress, step)
            
            elif status == 'finished':
                self.update_progress(85, "Download complete, processing audio...")
            
            elif status == 'error':
                logger.error(f"Download error in progress hook: {d.get('error', 'Unknown')}")
        
        except Exception as e:
            logger.error(f"Progress hook error: {e}")
    
    @staticmethod
    def _format_bytes(bytes_count: int) -> str:
        """Format bytes to human-readable string"""
        if bytes_count < 1024:
            return f"{bytes_count}B"
        elif bytes_count < 1024 ** 2:
            return f"{bytes_count / 1024:.1f}KB"
        elif bytes_count < 1024 ** 3:
            return f"{bytes_count / (1024 ** 2):.1f}MB"
        else:
            return f"{bytes_count / (1024 ** 3):.2f}GB"
    
    def download(self) -> str:
        """
        Download media using yt-dlp.
        Returns path to downloaded audio file.
        """
        try:
            import yt_dlp
        except ImportError:
            raise DownloadError(
                "yt-dlp not installed. Run: pip install yt-dlp"
            )
        
        self.update_progress(5, "Initializing download...")
        
        try:
            options = self._get_yt_dlp_options()
            
            with yt_dlp.YoutubeDL(options) as ydl:
                # Extract info first (faster than download)
                self.update_progress(10, "Extracting video information...")
                info = ydl.extract_info(self.task.url, download=False)
                
                # Store metadata in task
                self.task.original_title = info.get('title', '')
                self.task.original_artist = info.get('uploader', '') or info.get('channel', '')
                self.task.duration = info.get('duration')
                self.task.save(update_fields=['original_title', 'original_artist', 'duration'])
                
                self.update_progress(15, "Starting download...")
                
                # Download and convert
                ydl.download([self.task.url])
                
                # Find the downloaded file
                self.update_progress(90, "Locating downloaded file...")
                downloaded_file = self._find_downloaded_file()
                
                if not downloaded_file or not os.path.exists(downloaded_file):
                    raise DownloadError("Downloaded file not found")
                
                logger.info(f"Download complete: {downloaded_file}")
                return downloaded_file
        
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            logger.error(f"yt-dlp download error: {error_msg}")
            raise DownloadError(f"Download failed: {error_msg}")
        
        except Exception as e:
            logger.error(f"Unexpected download error: {e}", exc_info=True)
            raise DownloadError(f"Unexpected error: {str(e)}")
    
    def _find_downloaded_file(self) -> Optional[str]:
        """Find the downloaded file in temp directory"""
        task_id_str = str(self.task.id)
        
        # Look for files starting with task ID
        for filename in os.listdir(self.temp_dir):
            if filename.startswith(task_id_str):
                file_path = os.path.join(self.temp_dir, filename)
                
                # Check if it's the audio file (not thumbnail)
                if filename.endswith(('.mp3', '.flac', '.ogg', '.m4a', '.wav')):
                    return file_path
        
        return None
    
    def extract_metadata(self, file_path: str) -> Dict[str, any]:
        """
        Extract metadata from downloaded audio file using mutagen.
        """
        try:
            from mutagen import File as MutagenFile
        except ImportError:
            logger.warning("Mutagen not installed, skipping metadata extraction")
            return {}
        
        try:
            audio = MutagenFile(file_path, easy=True)
            if not audio:
                return {}
            
            metadata = {
                'title': audio.get('title', [self.task.original_title])[0],
                'artist': audio.get('artist', [self.task.original_artist])[0],
                'album': audio.get('album', [''])[0],
                'duration': int(audio.info.length) if hasattr(audio, 'info') else self.task.duration,
                'bitrate': int(audio.info.bitrate / 1000) if hasattr(audio, 'info') and hasattr(audio.info, 'bitrate') else None,
            }
            
            # Fallback to task metadata if empty
            if not metadata['title']:
                metadata['title'] = self.task.original_title or 'Unknown Title'
            if not metadata['artist']:
                metadata['artist'] = self.task.original_artist or 'Unknown Artist'
            
            return metadata
        
        except Exception as e:
            logger.error(f"Metadata extraction error: {e}")
            return {
                'title': self.task.original_title or 'Unknown Title',
                'artist': self.task.original_artist or 'Unknown Artist',
            }


def get_downloader(task: DownloadTask, progress_callback: Optional[Callable] = None) -> BaseDownloader:
    """
    Factory function to get appropriate downloader for task.
    
    Args:
        task: DownloadTask instance
        progress_callback: Optional callback function for progress updates
    
    Returns:
        BaseDownloader instance
    """
    # Currently only YouTube downloader (supports YouTube, SoundCloud, Bandcamp)
    # Can add more specialized downloaders in the future
    return YouTubeDownloader(task, progress_callback)


def create_music_file_from_download(task: DownloadTask, file_path: str, metadata: Dict) -> MusicFile:
    """
    Create MusicFile object from downloaded file.
    
    Args:
        task: DownloadTask that completed
        file_path: Path to downloaded audio file
        metadata: Extracted metadata dict
    
    Returns:
        Created MusicFile instance
    """
    try:
        # Get or create artist
        artist_name = metadata.get('artist', 'Unknown Artist')
        artist, _ = Artist.objects.get_or_create(name=artist_name)
        
        # Create MusicFile
        with open(file_path, 'rb') as f:
            music_file = MusicFile.objects.create(
                title=metadata.get('title', 'Unknown Title'),
                artist=artist,
                format=task.output_format,
                duration=metadata.get('duration', 0),
                bitrate=metadata.get('bitrate'),
            )
            
            # Attach file
            filename = f"{music_file.id}.{task.output_format}"
            music_file.file.save(filename, File(f), save=True)
        
        logger.info(f"Created MusicFile {music_file.id} from download task {task.id}")
        return music_file
    
    except Exception as e:
        logger.error(f"Error creating MusicFile from download: {e}", exc_info=True)
        raise
