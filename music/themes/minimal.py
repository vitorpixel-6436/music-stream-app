"""
Minimal Clean Theme

Simple, fast, minimalist design.
"""

from .base import BaseTheme


class MinimalTheme(BaseTheme):
    """Minimalist clean theme"""
    
    name = 'minimal'
    display_name = 'Minimal Clean'
    description = 'Simple and fast minimalist design'
    author = 'Music Stream Team'
    version = '1.0.0'
    
    def get_static_css(self):
        return [
            'css/minimal-theme.css',
        ]
    
    def get_static_js(self):
        return []  # No JS needed for minimal theme
    
    def get_card_template(self):
        return 'music/components/card_base.html'
    
    def get_theme_config(self):
        return {
            'card_aspect_ratio': '1/1',
            'grid_columns': 'repeat(auto-fill, minmax(200px, 1fr))',
            'animation_speed': 'none',
            'glass_effect': False,
            'carousel_enabled': False,
            'featured_banner': False,
        }
