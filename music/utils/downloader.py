"""Media download and processing utilities"""

import os
import re
import logging
import subprocess
from pathlib import Path
from typing import Dict, Optional, Tuple
from urllib.parse import urlparse, parse_qs

import yt_dlp
from django.conf import settings
from django.core.files import File
from mutagen import File as MutagenFile

logger = logging.getLogger(__name__)


class MediaDownloader:
    """Handle media downloads from various sources"""
    
    SUPPORTED_SOURCES = {
        'youtube': ['youtube.com', 'youtu.be', 'm.youtube.com'],
        'soundcloud': ['soundcloud.com', 'm.soundcloud.com'],
        'bandcamp': ['bandcamp.com'],
    }
    
    def __init__(self, download_dir: Optional[Path] = None):
        self.download_dir = download_dir or Path(settings.MEDIA_ROOT) / 'downloads' / 'temp'
        self.download_dir.mkdir(parents=True, exist_ok=True)
    
    def detect_source(self, url: str) -> str:
        """Detect the source platform from URL"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        for source, domains in self.SUPPORTED_SOURCES.items():
            if any(d in domain for d in domains):
                return source
        
        return 'url'
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL"""
        if 'youtube.com' in url or 'youtu.be' in url:
            patterns = [
                r'(?:youtube\.com\/watch\?v=)([\w-]+)',
                r'(?:youtu\.be\/)([\w-]+)',
                r'(?:youtube\.com\/embed\/)([\w-]+)',
            ]
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1)
        return None
    
    def get_video_info(self, url: str) -> Optional[Dict]:
        """Extract video metadata without downloading"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    'title': info.get('title', ''),
                    'artist': info.get('uploader', '') or info.get('artist', ''),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'description': info.get('description', ''),
                    'upload_date': info.get('upload_date', ''),
                }
        except Exception as e:
            logger.error(f"Failed to extract info from {url}: {e}")
            return None
    
    def download_audio(self, url: str, output_format: str = 'mp3', 
                      quality: str = '320', progress_callback=None) -> Optional[Path]:
        """Download audio from URL"""
        
        output_template = str(self.download_dir / '%(id)s.%(ext)s')
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'quiet': False,
            'no_warnings': False,
            'extract_audio': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': output_format,
                'preferredquality': quality,
            }],
            'progress_hooks': [progress_callback] if progress_callback else [],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_id = info.get('id', 'download')
                
                # Find downloaded file
                possible_files = list(self.download_dir.glob(f"{video_id}.*"))
                
                for file_path in possible_files:
                    if file_path.suffix.lower() in ['.mp3', '.flac', '.wav', '.m4a', '.ogg']:
                        return file_path
                
                logger.error(f"Downloaded file not found for {url}")
                return None
                
        except Exception as e:
            logger.error(f"Download failed for {url}: {e}")
            return None
    
    def extract_metadata(self, file_path: Path) -> Dict:
        """Extract metadata from audio file using mutagen"""
        try:
            audio = MutagenFile(file_path)
            
            if audio is None:
                return {}
            
            metadata = {
                'duration': int(audio.info.length) if hasattr(audio.info, 'length') else 0,
                'bitrate': int(audio.info.bitrate / 1000) if hasattr(audio.info, 'bitrate') else 0,
                'sample_rate': getattr(audio.info, 'sample_rate', 0),
                'channels': getattr(audio.info, 'channels', 0),
            }
            
            # Try to extract tags
            if hasattr(audio, 'tags') and audio.tags:
                tags = audio.tags
                metadata['title'] = str(tags.get('title', [''])[0]) if 'title' in tags else ''
                metadata['artist'] = str(tags.get('artist', [''])[0]) if 'artist' in tags else ''
                metadata['album'] = str(tags.get('album', [''])[0]) if 'album' in tags else ''
            
            return metadata
            
        except Exception as e:
            logger.error(f"Metadata extraction failed for {file_path}: {e}")
            return {}
    
    def cleanup_file(self, file_path: Path):
        """Remove temporary file"""
        try:
            if file_path.exists():
                file_path.unlink()
                logger.info(f"Cleaned up temp file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to cleanup {file_path}: {e}")
    
    def validate_url(self, url: str) -> Tuple[bool, str]:
        """Validate if URL is downloadable"""
        try:
            source = self.detect_source(url)
            
            if source == 'url':
                return False, "Unsupported URL. Please use YouTube, SoundCloud, or Bandcamp links."
            
            # Quick check without full download
            info = self.get_video_info(url)
            
            if info is None:
                return False, "Unable to extract video information. URL may be invalid or restricted."
            
            # Check duration (max 1 hour for free tier)
            if info.get('duration', 0) > 3600:
                return False, "Video duration exceeds 1 hour limit."
            
            return True, "URL is valid"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"


class DownloadProgressTracker:
    """Track download progress for callbacks"""
    
    def __init__(self, task_id, update_callback):
        self.task_id = task_id
        self.update_callback = update_callback
        self.last_progress = 0
    
    def __call__(self, d):
        """Called by yt-dlp with progress updates"""
        if d['status'] == 'downloading':
            try:
                percent_str = d.get('_percent_str', '0%')
                percent = float(percent_str.strip('%'))
                
                # Only update if progress changed significantly
                if abs(percent - self.last_progress) >= 1:
                    self.last_progress = percent
                    self.update_callback(int(percent), f"Downloading: {percent:.1f}%")
                    
            except (ValueError, KeyError):
                pass
        
        elif d['status'] == 'finished':
            self.update_callback(90, "Download complete, processing...")
        
        elif d['status'] == 'error':
            logger.error(f"Download error for task {self.task_id}: {d.get('error', 'Unknown')}")


def get_format_from_url(url: str) -> str:
    """Detect preferred output format based on source"""
    source = MediaDownloader().detect_source(url)
    
    # Default formats per source
    format_map = {
        'youtube': 'mp3',
        'soundcloud': 'mp3',
        'bandcamp': 'flac',  # Bandcamp often has high quality
    }
    
    return format_map.get(source, 'mp3')
