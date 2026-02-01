"""
Steam UI Configuration
======================

Global configuration for Steam UI Framework.
Can be customized per project.
"""

from typing import Dict, Any


class SteamUIConfig:
    """
    Configuration class for Steam UI Framework.
    
    Usage:
        from steam_ui.config import config
        config.STATIC_URL = '/custom/static/'
    """
    
    # Static files configuration
    STATIC_URL: str = '/static/steam_ui/'
    STATIC_ROOT: str = 'steam_ui/static/'
    
    # CDN support (optional)
    USE_CDN: bool = False
    CDN_URL: str = ''
    
    # Template configuration
    TEMPLATE_DIR: str = 'steam_ui/templates/'
    
    # Feature flags
    ENABLE_ANIMATIONS: bool = True
    ENABLE_GLASS_EFFECTS: bool = True
    ENABLE_AUTO_PLAY: bool = False
    
    # Performance
    LAZY_LOAD_IMAGES: bool = True
    PRELOAD_COVERS: int = 6  # Number of images to preload
    
    # Colors & Theme
    PRIMARY_COLOR: str = '#e31837'  # Steam red
    GLASS_BLUR: str = '20px'
    GLASS_OPACITY: float = 0.08
    
    # Grid settings
    DEFAULT_GRID_COLUMNS: int = 4
    DEFAULT_GRID_GAP: str = '32px'
    
    # Carousel settings
    CAROUSEL_AUTO_SCROLL: bool = False
    CAROUSEL_SCROLL_INTERVAL: int = 5000  # ms
    
    @classmethod
    def update(cls, **kwargs):
        """Update configuration values."""
        for key, value in kwargs.items():
            if hasattr(cls, key):
                setattr(cls, key, value)
    
    @classmethod
    def get_static_url(cls, path: str) -> str:
        """Get full static file URL."""
        if cls.USE_CDN and cls.CDN_URL:
            return f"{cls.CDN_URL.rstrip('/')}/{path.lstrip('/')}"
        return f"{cls.STATIC_URL.rstrip('/')}/{path.lstrip('/')}"
    
    @classmethod
    def as_dict(cls) -> Dict[str, Any]:
        """Export config as dictionary."""
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if key.isupper() and not key.startswith('_')
        }


# Global config instance
config = SteamUIConfig()
