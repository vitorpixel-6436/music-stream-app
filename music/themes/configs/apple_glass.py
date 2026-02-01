"""
Apple Glass Theme

Clean, minimal theme inspired by Apple's design language.
Focuses on glass morphism and subtle animations.
"""

from music.themes.base import BaseTheme, Component


class AppleGlassTheme(BaseTheme):
    """
    Apple Glass Theme - Clean, minimal, sophisticated
    
    Features:
    - Heavy glass morphism
    - Subtle animations
    - White/blue color scheme
    - Rounded corners
    """
    
    name = 'apple_glass'
    display_name = 'Apple Glass'
    description = 'Clean minimal theme with heavy glass morphism effects'
    author = 'Music Stream Team'
    version = '1.0.0'
    
    colors = {
        'primary': '#007aff',
        'primary_dark': '#0051d5',
        'secondary': '#5ac8fa',
        'background': '#f5f5f7',
        'surface': 'rgba(255, 255, 255, 0.7)',
        'surface_hover': 'rgba(255, 255, 255, 0.85)',
        'text': '#1d1d1f',
        'text_secondary': 'rgba(29, 29, 31, 0.7)',
        'text_muted': 'rgba(29, 29, 31, 0.4)',
        'border': 'rgba(0, 0, 0, 0.1)',
        'shadow': 'rgba(0, 0, 0, 0.1)',
    }
    
    fonts = {
        'primary': '-apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif',
        'heading': '-apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif',
        'mono': '"SF Mono", Monaco, monospace',
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
        """Register all Apple Glass theme components"""
        
        # Card Component
        self.register_component(Component(
            name='card',
            template='themes/apple_glass/components/card.html',
            css=['themes/apple_glass/cards.css'],
            js=[]
        ))
        
        # Carousel Component
        self.register_component(Component(
            name='carousel',
            template='themes/apple_glass/components/carousel.html',
            css=['themes/apple_glass/carousel.css'],
            js=['themes/apple_glass/carousel.js']
        ))
    
    def get_css_files(self):
        return [
            'css/glass-liquid.css',
            'themes/apple_glass/style.css',
        ]
    
    def get_js_files(self):
        return [
            'themes/apple_glass/main.js',
        ]
