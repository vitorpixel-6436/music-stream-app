"""
Music Stream UI Theme System

Simple theme framework for rapid UI development.
"""

from .registry import ThemeRegistry
from .base import BaseTheme

# Auto-register available themes
registry = ThemeRegistry()

__all__ = ['ThemeRegistry', 'BaseTheme', 'registry']
