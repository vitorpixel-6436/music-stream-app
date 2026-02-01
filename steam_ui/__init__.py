"""
Steam UI Framework
==================

A modular, reusable UI component library inspired by Steam's design language.

Features:
- Glass morphism effects
- Animated cards and carousels
- Responsive grid layouts
- Django template integration
- Standalone usage support

Version: 1.0.0
Author: vitorpixel-6436
License: MIT
"""

__version__ = '1.0.0'
__author__ = 'vitorpixel-6436'

# Import main components for easy access
from steam_ui.components import (
    Card,
    Carousel,
    FeaturedBanner,
    CategoryPills,
)

__all__ = [
    'Card',
    'Carousel', 
    'FeaturedBanner',
    'CategoryPills',
]
