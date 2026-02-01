"""
Steam UI Components
===================

Base component classes for Steam UI Framework.
Each component encapsulates rendering logic and can be used
both in Django templates and standalone Python code.
"""

from typing import Dict, Any, List, Optional
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class BaseComponent:
    """
    Base class for all UI components.
    
    Provides common rendering functionality and context management.
    """
    
    template_name: str = None
    
    def __init__(self, **kwargs):
        self.extra_context = kwargs
    
    def get_context(self, **kwargs) -> Dict[str, Any]:
        """Build context for template rendering."""
        context = self.extra_context.copy()
        context.update(kwargs)
        return context
    
    def render(self, **kwargs) -> str:
        """Render component to HTML string."""
        if not self.template_name:
            raise NotImplementedError("template_name must be defined")
        
        context = self.get_context(**kwargs)
        return mark_safe(render_to_string(self.template_name, context))
    
    def __str__(self) -> str:
        return self.render()


class Card(BaseComponent):
    """
    Steam-style track card component.
    
    Usage:
        card = Card()
        html = card.render(track=track_object)
    
    Template variables:
        - track: Track object with title, artist, cover_image, etc.
        - show_actions: bool, show action buttons (default: True)
        - size: str, card size variant ('normal', 'large', 'small')
    """
    
    template_name = 'steam_ui/card.html'
    
    def __init__(self, show_actions=True, size='normal', **kwargs):
        super().__init__(**kwargs)
        self.show_actions = show_actions
        self.size = size
    
    def get_context(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context(**kwargs)
        context.setdefault('show_actions', self.show_actions)
        context.setdefault('size', self.size)
        return context


class Carousel(BaseComponent):
    """
    Steam-style carousel component.
    
    Usage:
        carousel = Carousel(title="Recently Added")
        html = carousel.render(tracks=track_list)
    
    Template variables:
        - tracks: List of track objects
        - title: str, carousel section title
        - icon: str, FontAwesome icon class
        - show_navigation: bool, show arrow buttons
    """
    
    template_name = 'steam_ui/carousel.html'
    
    def __init__(self, title="Tracks", icon="fa-music", show_navigation=True, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.icon = icon
        self.show_navigation = show_navigation
    
    def get_context(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context(**kwargs)
        context.setdefault('title', self.title)
        context.setdefault('icon', self.icon)
        context.setdefault('show_navigation', self.show_navigation)
        return context


class FeaturedBanner(BaseComponent):
    """
    Steam-style featured banner (hero section).
    
    Usage:
        banner = FeaturedBanner()
        html = banner.render(track=featured_track)
    
    Template variables:
        - track: Featured track object
        - show_description: bool, show description text
        - cta_primary: str, primary button text
        - cta_secondary: str, secondary button text
    """
    
    template_name = 'steam_ui/featured.html'
    
    def __init__(self, show_description=True, cta_primary="Play Now", cta_secondary="Download", **kwargs):
        super().__init__(**kwargs)
        self.show_description = show_description
        self.cta_primary = cta_primary
        self.cta_secondary = cta_secondary
    
    def get_context(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context(**kwargs)
        context.setdefault('show_description', self.show_description)
        context.setdefault('cta_primary', self.cta_primary)
        context.setdefault('cta_secondary', self.cta_secondary)
        return context


class CategoryPills(BaseComponent):
    """
    Category filter pills component.
    
    Usage:
        pills = CategoryPills()
        html = pills.render(categories=category_list, active='all')
    
    Template variables:
        - categories: List of category dicts with 'id', 'name', 'icon'
        - active: str, currently active category id
    """
    
    template_name = 'steam_ui/category_pills.html'
    
    def get_context(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context(**kwargs)
        context.setdefault('active', 'all')
        return context


class Grid(BaseComponent):
    """
    Responsive grid layout container.
    
    Usage:
        grid = Grid(columns=4)
        html = grid.render(items=track_list, component=Card())
    
    Template variables:
        - items: List of items to render
        - component: Component instance to render each item
        - columns: int, number of columns (responsive)
    """
    
    template_name = 'steam_ui/grid.html'
    
    def __init__(self, columns=4, gap='32px', **kwargs):
        super().__init__(**kwargs)
        self.columns = columns
        self.gap = gap
    
    def get_context(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context(**kwargs)
        context.setdefault('columns', self.columns)
        context.setdefault('gap', self.gap)
        return context
