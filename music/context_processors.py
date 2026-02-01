"""
Context Processors for Music App

Provides global context variables for all templates.
"""

from music.themes import ThemeRegistry


def theme_context(request):
    """
    Add theme information to template context.
    
    Usage in template:
        {{ current_theme.display_name }}
        {{ current_theme.colors.primary }}
    """
    return {
        'current_theme': ThemeRegistry.get_active_theme(),
        'all_themes': ThemeRegistry.get_all_themes(),
    }
