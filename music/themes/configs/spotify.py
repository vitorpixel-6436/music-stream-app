"""
Spotify Minimal Theme

Minimalist theme inspired by Spotify's clean interface.
Dark mode with green accents.
"""

from music.themes.base import BaseTheme, Component


class SpotifyTheme(BaseTheme):
    """
    Spotify Minimal Theme - Dark, clean, focused
    
    Features:
    - Dark background
    - Green accents
    - Minimal design
    - Focus on content
    """
    
    name = 'spotify'
    display_name = 'Spotify Minimal'
    description = 'Dark minimal theme inspired by Spotify'
    author = 'Music Stream Team'
    version = '1.0.0'
    
    colors = {
        'primary': '#1db954',
        'primary_dark': '#1aa34a',
        'secondary': '#1ed760',
        'background': '#121212',
        'surface': '#181818',
        'surface_hover': '#282828',
        'text': '#ffffff',
        'text_secondary': '#b3b3b3',
        'text_muted': '#535353',
        'border': '#282828',
        'shadow': 'rgba(0, 0, 0, 0.5)',
    }
    
    fonts = {
        'primary': 'Circular, -apple-system, BlinkMacSystemFont, sans-serif',
        'heading': 'Circular, -apple-system, BlinkMacSystemFont, sans-serif',
        'mono': 'Consolas, "Courier New", monospace',
    }
    
    spacing = {
        'xs': '0.25rem',
        'sm': '0.5rem',
        'md': '1rem',
        'lg': '1.5rem',
        'xl': '2rem',
        '2xl': '3rem',
        '3xl': '4rem',
    }
    
    def _register_components(self):
        """Register all Spotify theme components"""
        
        # Card Component
        self.register_component(Component(
            name='card',
            template='themes/spotify/components/card.html',
            css=['css/spotify-minimal.css'],
            js=['js/spotify-minimal.js']
        ))
        
        # Playlist Component
        self.register_component(Component(
            name='playlist',
            template='themes/spotify/components/playlist.html',
            css=['css/spotify-minimal.css'],
            js=[]
        ))
    
    def get_css_files(self):
        return [
            'css/spotify-minimal.css',
        ]
    
    def get_js_files(self):
        return [
            'js/spotify-minimal.js',
        ]
