"""
Theme Registry

Manages theme registration and retrieval.
"""

from typing import Dict, Optional, List
from django.conf import settings
import importlib
import logging

logger = logging.getLogger(__name__)


class ThemeRegistry:
    """
    Singleton registry for managing themes.
    
    Usage:
        # Register theme
        ThemeRegistry.register('steam', 'music.themes.configs.steam.SteamTheme')
        
        # Get active theme
        theme = ThemeRegistry.get_active_theme()
        
        # List all themes
        themes = ThemeRegistry.get_all_themes()
    """
    
    _themes: Dict[str, str] = {}  # name -> import_path
    _instances: Dict[str, 'BaseTheme'] = {}  # name -> theme_instance
    _active_theme: Optional[str] = None
    
    @classmethod
    def register(cls, name: str, import_path: str):
        """Register a theme by name and import path"""
        cls._themes[name] = import_path
        logger.info(f"Registered theme: {name} -> {import_path}")
    
    @classmethod
    def register_theme_class(cls, theme_class):
        """Register a theme class directly"""
        instance = theme_class()
        cls._themes[instance.name] = f"{theme_class.__module__}.{theme_class.__name__}"
        cls._instances[instance.name] = instance
        logger.info(f"Registered theme class: {instance.name}")
    
    @classmethod
    def get_theme(cls, name: str) -> Optional['BaseTheme']:
        """Get theme instance by name"""
        # Check if already instantiated
        if name in cls._instances:
            return cls._instances[name]
        
        # Check if registered
        if name not in cls._themes:
            logger.warning(f"Theme '{name}' not registered")
            return None
        
        # Lazy load theme
        try:
            import_path = cls._themes[name]
            module_path, class_name = import_path.rsplit('.', 1)
            module = importlib.import_module(module_path)
            theme_class = getattr(module, class_name)
            instance = theme_class()
            cls._instances[name] = instance
            return instance
        except Exception as e:
            logger.error(f"Failed to load theme '{name}': {e}")
            return None
    
    @classmethod
    def get_active_theme(cls) -> Optional['BaseTheme']:
        """Get currently active theme"""
        if not cls._active_theme:
            # Get from settings
            cls._active_theme = getattr(settings, 'ACTIVE_THEME', 'steam')
        
        return cls.get_theme(cls._active_theme)
    
    @classmethod
    def set_active_theme(cls, name: str):
        """Set active theme"""
        if name not in cls._themes:
            raise ValueError(f"Theme '{name}' not registered")
        cls._active_theme = name
        logger.info(f"Active theme set to: {name}")
    
    @classmethod
    def get_all_themes(cls) -> List['BaseTheme']:
        """Get all registered themes"""
        return [cls.get_theme(name) for name in cls._themes.keys()]
    
    @classmethod
    def get_theme_names(cls) -> List[str]:
        """Get list of registered theme names"""
        return list(cls._themes.keys())
    
    @classmethod
    def clear(cls):
        """Clear all registered themes (mainly for testing)"""
        cls._themes.clear()
        cls._instances.clear()
        cls._active_theme = None
        logger.info("Theme registry cleared")
