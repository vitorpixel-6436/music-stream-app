from django.apps import AppConfig


class MusicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'music'

    def ready(self):
        """Initialize themes when app loads"""
        from music.themes import registry
        from music.themes.steam import SteamTheme
        from music.themes.minimal import MinimalTheme
        
        # Register all themes
        registry.register(SteamTheme)
        registry.register(MinimalTheme)
        
        # Set default theme (можно сделать через settings)
        registry.set_active_theme('steam')
