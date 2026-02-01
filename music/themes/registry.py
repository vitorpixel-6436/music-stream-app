"""
Theme Registry

Central registry for all available themes.
"""

class ThemeRegistry:
    """Registry for managing UI themes"""
    
    def __init__(self):
        self._themes = {}
        self._active_theme = None
    
    def register(self, theme_class):
        """Register a theme class"""
        theme_instance = theme_class()
        self._themes[theme_instance.name] = theme_instance
        return theme_instance
    
    def get_theme(self, name):
        """Get theme by name"""
        return self._themes.get(name)
    
    def get_active_theme(self):
        """Get currently active theme"""
        if not self._active_theme:
            # Default to first registered theme
            if self._themes:
                self._active_theme = list(self._themes.values())[0]
        return self._active_theme
    
    def set_active_theme(self, name):
        """Set active theme by name"""
        theme = self.get_theme(name)
        if theme:
            self._active_theme = theme
            return True
        return False
    
    def list_themes(self):
        """List all registered themes"""
        return [
            {
                'name': theme.name,
                'display_name': theme.display_name,
                'description': theme.description,
                'author': theme.author,
                'version': theme.version,
            }
            for theme in self._themes.values()
        ]
