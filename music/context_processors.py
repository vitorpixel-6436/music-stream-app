"""
Context Processors

Make theme available in all templates.
"""

from music.themes import registry


def theme_context(request):
    """Add active theme to template context"""
    theme = registry.get_active_theme()
    
    return {
        'theme': theme,
        'theme_name': theme.name if theme else 'base',
        'theme_css': theme.get_static_css() if theme else [],
        'theme_js': theme.get_static_js() if theme else [],
    }
