"""
Steam Gaming Theme

A bold, gaming-inspired theme with glass morphism effects.
Perfect for music streaming with high-energy aesthetics.
"""

from music.themes.base import BaseTheme, Component


class SteamTheme(BaseTheme):
    """
    Steam Gaming Theme - Bold, modern, gaming-inspired
    
    Features:
    - Glass morphism effects
    - High contrast cards
    - Animated hover states
    - Red/black color scheme
    """
    
    name = 'steam'
    display_name = 'Steam Gaming'
    description = 'Bold gaming-inspired theme with glass morphism effects'
    author = 'Music Stream Team'
    version = '2.1.0'
    
    colors = {
        'primary': '#e31837',
        'primary_dark': '#b01029',
        'secondary': '#ff3355',
        'background': '#0a0a0a',
        'surface': 'rgba(255, 255, 255, 0.08)',
        'surface_hover': 'rgba(255, 255, 255, 0.12)',
        'text': '#ffffff',
        'text_secondary': 'rgba(255, 255, 255, 0.7)',
        'text_muted': 'rgba(255, 255, 255, 0.4)',
        'border': 'rgba(255, 255, 255, 0.1)',
        'shadow': 'rgba(0, 0, 0, 0.6)',
    }
    
    fonts = {
        'primary': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        'heading': '"Inter", -apple-system, BlinkMacSystemFont, sans-serif',
        'mono': '"JetBrains Mono", "Courier New", monospace',
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
        """Register all Steam theme components"""
        
        # Card Component
        self.register_component(Component(
            name='card',
            template='themes/steam/components/card.html',
            css=['css/steam-cards.css'],
            js=['js/steam-cards.js']
        ))
        
        # Carousel Component
        self.register_component(Component(
            name='carousel',
            template='themes/steam/components/carousel.html',
            css=['css/steam-carousel.css'],
            js=['js/steam-carousel.js']
        ))
        
        # Featured Banner Component
        self.register_component(Component(
            name='featured',
            template='themes/steam/components/featured.html',
            css=['css/steam-cards.css'],
            js=[]
        ))
        
        # Player Component
        self.register_component(Component(
            name='player',
            template='themes/steam/components/player.html',
            css=['css/glass-dynamics.css', 'music/css/style.css'],
            js=['js/glass-dynamics.js']
        ))
        
        # Grid Component
        self.register_component(Component(
            name='grid',
            template='themes/steam/components/grid.html',
            css=['css/steam-cards.css'],
            js=[]
        ))
    
    def get_css_files(self):
        """Get all CSS files for Steam theme"""
        return [
            # Base glass system
            'css/glass-liquid.css',
            'css/glass-dynamics.css',
            
            # Steam components
            'css/steam-cards.css',
            'css/steam-carousel.css',
            
            # MSI Gaming elements
            'css/msi-gaming.css',
            
            # Spotify minimal
            'css/spotify-minimal.css',
            
            # Main music styles
            'music/css/style.css',
        ]
    
    def get_js_files(self):
        """Get all JavaScript files for Steam theme"""
        return [
            'js/glass-dynamics.js',
            'js/steam-carousel.js',
            'js/spotify-minimal.js',
        ]
