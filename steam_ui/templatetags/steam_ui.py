"""
Steam UI Template Tags
======================

Django template tags for easy component usage.

Usage:
    {% load steam_ui %}
    {% steam_card track %}
    {% steam_carousel tracks title="Recent" %}
    {% steam_css %}
    {% steam_js %}
"""

from django import template
from django.utils.safestring import mark_safe
from steam_ui.components import Card, Carousel, FeaturedBanner, CategoryPills
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
