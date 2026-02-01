"""
Theme Template Tags

Django template tags for rendering themed components.

Usage:
    {% load theme_tags %}
    
    {# Load theme CSS/JS #}
    {% theme_css %}
    {% theme_js %}
    
    {# Render components #}
    {% theme_card track %}
    {% theme_carousel tracks title="Recently Added" %}
    {% theme_featured track %}
    
    {# Get theme config #}
    {% get_theme_config as config %}
    {{ config.colors.primary }}
"""

from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from music.themes import ThemeRegistry

register = template.Library()


@register.simple_tag
def theme_css():
    """Load all CSS files for active theme"""
    theme = ThemeRegistry.get_active_theme()
    if not theme:
        return ''
    
    css_files = theme.get_css_files()
    html = []
    for css_file in css_files:
        html.append(f'<link rel="stylesheet" href="/static/{css_file}">')
    
    return mark_safe('\n'.join(html))


@register.simple_tag
def theme_js():
    """Load all JavaScript files for active theme"""
    theme = ThemeRegistry.get_active_theme()
    if not theme:
        return ''
    
    js_files = theme.get_js_files()
    html = []
    for js_file in js_files:
        html.append(f'<script src="/static/{js_file}"></script>')
    
    return mark_safe('\n'.join(html))


@register.simple_tag
def component_css(component_name):
    """Load CSS files for specific component"""
    theme = ThemeRegistry.get_active_theme()
    if not theme:
        return ''
    
    css_files = theme.get_component_css(component_name)
    html = []
    for css_file in css_files:
        html.append(f'<link rel="stylesheet" href="/static/{css_file}">')
    
    return mark_safe('\n'.join(html))


@register.simple_tag
def component_js(component_name):
    """Load JS files for specific component"""
    theme = ThemeRegistry.get_active_theme()
    if not theme:
        return ''
    
    js_files = theme.get_component_js(component_name)
    html = []
    for js_file in js_files:
        html.append(f'<script src="/static/{js_file}"></script>')
    
    return mark_safe('\n'.join(html))


@register.inclusion_tag('themes/components/card.html', takes_context=True)
def theme_card(context, track, **kwargs):
    """Render a track card using active theme"""
    theme = ThemeRegistry.get_active_theme()
    return {
        'track': track,
        'theme': theme,
        'extra': kwargs,
    }


@register.inclusion_tag('themes/components/carousel.html', takes_context=True)
def theme_carousel(context, tracks, title=None, icon=None, **kwargs):
    """Render a carousel using active theme"""
    theme = ThemeRegistry.get_active_theme()
    return {
        'tracks': tracks,
        'title': title or 'Tracks',
        'icon': icon or 'fas fa-music',
        'theme': theme,
        'extra': kwargs,
    }


@register.inclusion_tag('themes/components/featured.html', takes_context=True)
def theme_featured(context, track, **kwargs):
    """Render a featured banner using active theme"""
    theme = ThemeRegistry.get_active_theme()
    return {
        'track': track,
        'theme': theme,
        'extra': kwargs,
    }


@register.simple_tag
def get_theme_config():
    """Get configuration for active theme"""
    theme = ThemeRegistry.get_active_theme()
    return theme.get_config() if theme else {}


@register.simple_tag
def get_theme():
    """Get active theme instance"""
    return ThemeRegistry.get_active_theme()


@register.simple_tag
def get_all_themes():
    """Get all available themes"""
    return ThemeRegistry.get_all_themes()


@register.filter
def theme_color(color_name):
    """Get color from theme palette"""
    theme = ThemeRegistry.get_active_theme()
    if theme and color_name in theme.colors:
        return theme.colors[color_name]
    return ''
