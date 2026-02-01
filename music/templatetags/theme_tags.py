"""
Theme Template Tags

Easy component rendering and theme utilities.
"""

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def theme_card(track, variant='default'):
    """Render a music card using active theme
    
    Usage:
        {% theme_card track %}
        {% theme_card track variant="compact" %}
    """
    from music.themes import registry
    theme = registry.get_active_theme()
    
    # Build card HTML (simplified for now)
    return mark_safe(f'''
        <div class="steam-card" data-track-id="{track.pk}">
            <!-- Card content -->
        </div>
    ''')


@register.simple_tag
def load_theme_assets():
    """Load all theme CSS and JS
    
    Usage:
        {% load_theme_assets %}
    """
    from music.themes import registry
    theme = registry.get_active_theme()
    
    if not theme:
        return ''
    
    html = []
    
    # CSS files
    for css in theme.get_static_css():
        html.append(f'<link rel="stylesheet" href="/static/{css}">')
    
    # JS files
    for js in theme.get_static_js():
        html.append(f'<script src="/static/{js}"></script>')
    
    return mark_safe('\n'.join(html))


@register.simple_tag
def theme_config(key, default=None):
    """Get theme configuration value
    
    Usage:
        {% theme_config 'card_aspect_ratio' '3/4' %}
    """
    from music.themes import registry
    theme = registry.get_active_theme()
    
    if not theme:
        return default
    
    config = theme.get_theme_config()
    return config.get(key, default)
