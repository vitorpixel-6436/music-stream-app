"""
Steam UI Template Tags
======================

Django template tags for easy component usage.

Usage:
    {% load steam_ui %}
    {% steam_card track %}
    {% steam_carousel tracks title="Recent" %}
    {% steam_player_bar current_track %}
    {% steam_playlist playlist %}
    {% steam_css %}
    {% steam_js %}
"""

from django import template
from django.utils.safestring import mark_safe
from steam_ui.components import (
    Card,
    Carousel,
    FeaturedBanner,
    CategoryPills,
    PlayerBar,
    Playlist,
)
from steam_ui.config import config

register = template.Library()


@register.simple_tag
def steam_css(*files):
    """
    Include Steam UI CSS files.
    
    Usage:
        {% steam_css %}  # All default CSS
        {% steam_css 'cards' 'carousel' %}  # Specific modules
    """
    if not files:
        # Default CSS files
        files = [
            'css/glass-liquid.css',
            'css/glass-dynamics.css',
            'css/steam-cards.css',
            'css/steam-carousel.css',
            'css/steam-player.css',
            'css/steam-playlist.css',
        ]
    else:
        # Add .css extension if missing
        files = [f if f.endswith('.css') else f'css/{f}.css' for f in files]
    
    links = []
    for file in files:
        url = config.get_static_url(file)
        links.append(f'<link rel="stylesheet" href="{url}">')
    
    return mark_safe('\n'.join(links))


@register.simple_tag
def steam_js(*files):
    """
    Include Steam UI JavaScript files.
    
    Usage:
        {% steam_js %}  # All default JS
        {% steam_js 'carousel' %}  # Specific module
    """
    if not files:
        # Default JS files
        files = [
            'js/glass-dynamics.js',
            'js/steam-carousel.js',
            'js/steam-player.js',
        ]
    else:
        # Add .js extension if missing
        files = [f if f.endswith('.js') else f'js/{f}.js' for f in files]
    
    scripts = []
    for file in files:
        url = config.get_static_url(file)
        scripts.append(f'<script src="{url}"></script>')
    
    return mark_safe('\n'.join(scripts))


@register.simple_tag
def steam_card(track, show_actions=True, size='normal'):
    """
    Render a Steam-style track card.
    
    Usage:
        {% steam_card track %}
        {% steam_card track show_actions=False %}
        {% steam_card track size='large' %}
    """
    card = Card(show_actions=show_actions, size=size)
    return card.render(track=track)


@register.simple_tag
def steam_carousel(tracks, title='Tracks', icon='fa-music', show_navigation=True):
    """
    Render a Steam-style carousel.
    
    Usage:
        {% steam_carousel tracks %}
        {% steam_carousel tracks title="Recently Added" icon="fa-clock" %}
    """
    carousel = Carousel(title=title, icon=icon, show_navigation=show_navigation)
    return carousel.render(tracks=tracks)


@register.simple_tag
def steam_featured(track, show_description=True, cta_primary='Play Now', cta_secondary='Download'):
    """
    Render a Steam-style featured banner.
    
    Usage:
        {% steam_featured track %}
        {% steam_featured track show_description=False %}
        {% steam_featured track cta_primary="Listen" %}
    """
    banner = FeaturedBanner(
        show_description=show_description,
        cta_primary=cta_primary,
        cta_secondary=cta_secondary
    )
    return banner.render(track=track)


@register.simple_tag
def steam_category_pills(categories, active='all'):
    """
    Render category filter pills.
    
    Usage:
        {% steam_category_pills categories %}
        {% steam_category_pills categories active='recent' %}
    """
    pills = CategoryPills()
    return pills.render(categories=categories, active=active)


@register.simple_tag
def steam_player_bar(current_track=None, show_queue=True, show_volume=True, autoplay=False):
    """
    Render floating audio player bar.
    
    Usage:
        {% steam_player_bar %}
        {% steam_player_bar current_track autoplay=True %}
        {% steam_player_bar current_track show_queue=False %}
    """
    player = PlayerBar(
        show_queue=show_queue,
        show_volume=show_volume,
        autoplay=autoplay
    )
    return player.render(current_track=current_track)


@register.simple_tag
def steam_playlist(playlist, mode='card', show_tracks=False, max_tracks=5):
    """
    Render playlist component.
    
    Usage:
        {% steam_playlist playlist %}
        {% steam_playlist playlist mode='list' %}
        {% steam_playlist playlist show_tracks=True max_tracks=10 %}
    """
    playlist_comp = Playlist(
        mode=mode,
        show_tracks=show_tracks,
        max_tracks=max_tracks
    )
    return playlist_comp.render(playlist=playlist)


@register.filter
def steam_config(key):
    """
    Get Steam UI config value.
    
    Usage:
        {{ 'PRIMARY_COLOR'|steam_config }}
    """
    return getattr(config, key, None)


@register.simple_tag(takes_context=True)
def steam_render_component(context, component, **kwargs):
    """
    Render a custom component with context.
    
    Usage:
        {% steam_render_component my_component track=track %}
    """
    # Merge template context with kwargs
    render_context = {**context.flatten(), **kwargs}
    return component.render(**render_context)
