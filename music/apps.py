from django.apps import AppConfig


class MusicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'music'

    def ready(self):
        """
        Initialize themes on app startup
        """
        # Import theme registry and theme classes
        from music.themes import ThemeRegistry
        from music.themes.configs.steam import SteamTheme
        from music.themes.configs.apple_glass import AppleGlassTheme
        from music.themes.configs.spotify import SpotifyTheme
        
        # Register all available themes
        ThemeRegistry.register_theme_class(SteamTheme)
        ThemeRegistry.register_theme_class(AppleGlassTheme)
        ThemeRegistry.register_theme_class(SpotifyTheme)
        
        # Set default active theme
        # This can be overridden in settings.py with ACTIVE_THEME
        ThemeRegistry.set_active_theme('steam')
        
        print("✅ Themes initialized:")
        for theme in ThemeRegistry.get_all_themes():
            print(f"   - {theme.display_name} (v{theme.version})")
        print(f"   Active: {ThemeRegistry.get_active_theme().display_name}")
