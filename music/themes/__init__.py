"""
Music Stream UI Framework

A modular theme system for rapid UI development and deployment.

Usage:
    from music.themes import ThemeRegistry
    
    # Get active theme
    theme = ThemeRegistry.get_active_theme()
    
    # In templates:
    {% load theme_tags %}
    {% theme_css %}
    {% theme_card track %}
"""

from .base import BaseTheme, Component
from .registry import ThemeRegistry

__all__ = ['BaseTheme', 'Component', 'ThemeRegistry']
__version__ = '1.0.0'
