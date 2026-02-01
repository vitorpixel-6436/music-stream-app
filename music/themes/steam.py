"""
Steam Gaming Theme

Modern gaming-inspired UI with Steam library aesthetics.
"""

from .base import BaseTheme


class SteamTheme(BaseTheme):
    """Steam-style gaming theme"""
    
    name = 'steam'
    display_name = 'Steam Gaming'
    description = 'Modern gaming UI inspired by Steam library'
    author = 'Music Stream Team'
    version = '2.1.0'
    
    def get_static_css(self):
        return [
            'css/steam-cards.css',
            'css/steam-carousel.css',
            'css/glass-dynamics.css',
            'css/glass-liquid.css',
        ]
    
    def get_static_js(self):
        return [
            'js/steam-carousel.js',
            'js/glass-dynamics.js',
        ]
    
    def get_card_template(self):
        return 'music/themes/steam/card.html'
    
    def get_index_template(self):
        return 'music/index.html'  # Already Steam-styled
    
    def get_theme_config(self):
        return {
            'card_aspect_ratio': '3/4',
            'grid_columns': 'repeat(auto-fill, minmax(320px, 1fr))',
            'animation_speed': 'fast',
            'glass_effect': True,
            'carousel_enabled': True,
            'featured_banner': True,
        }
