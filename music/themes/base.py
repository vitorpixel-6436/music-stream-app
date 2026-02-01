"""
Base Theme Classes

Provides abstract base classes for creating custom themes.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import os


class Component:
    """Base component class for UI elements"""
    
    def __init__(self, name: str, template: str, css: List[str] = None, js: List[str] = None):
        self.name = name
        self.template = template
        self.css = css or []
        self.js = js or []
    
    def __repr__(self):
        return f"Component('{self.name}', template='{self.template}')"


class BaseTheme(ABC):
    """
    Abstract base class for all themes.
    
    Each theme must implement:
    - name: Unique theme identifier
    - display_name: Human-readable theme name
    - description: Theme description
    - author: Theme author
    - version: Theme version
    
    Optional customizations:
    - colors: Color palette
    - fonts: Font configuration
    - spacing: Spacing system
    - components: Custom components
    """
    
    # Required attributes
    name: str = None
    display_name: str = None
    description: str = None
    author: str = None
    version: str = "1.0.0"
    
    # Optional customizations
    colors: Dict[str, str] = {}
    fonts: Dict[str, str] = {}
    spacing: Dict[str, str] = {}
    
    def __init__(self):
        if not self.name:
            raise ValueError(f"{self.__class__.__name__} must define 'name' attribute")
        if not self.display_name:
            self.display_name = self.name.replace('_', ' ').title()
        
        self._components = {}
        self._register_components()
    
    @abstractmethod
    def _register_components(self):
        """Register theme components. Override in subclass."""
        pass
    
    def register_component(self, component: Component):
        """Register a UI component"""
        self._components[component.name] = component
    
    def get_component(self, name: str) -> Optional[Component]:
        """Get component by name"""
        return self._components.get(name)
    
    def get_all_components(self) -> Dict[str, Component]:
        """Get all registered components"""
        return self._components.copy()
    
    # CSS Management
    def get_css_files(self) -> List[str]:
        """Get list of CSS files for this theme"""
        return [
            f'themes/{self.name}/style.css',
        ]
    
    def get_component_css(self, component_name: str) -> List[str]:
        """Get CSS files for specific component"""
        component = self.get_component(component_name)
        return component.css if component else []
    
    # JS Management
    def get_js_files(self) -> List[str]:
        """Get list of JavaScript files for this theme"""
        return [
            f'themes/{self.name}/main.js',
        ]
    
    def get_component_js(self, component_name: str) -> List[str]:
        """Get JS files for specific component"""
        component = self.get_component(component_name)
        return component.js if component else []
    
    # Template Management
    def get_template_path(self, template_name: str) -> str:
        """Get template path for this theme"""
        return f'themes/{self.name}/{template_name}'
    
    def get_component_template(self, component_name: str) -> Optional[str]:
        """Get template path for specific component"""
        component = self.get_component(component_name)
        return component.template if component else None
    
    # Configuration
    def get_config(self) -> Dict:
        """Get theme configuration"""
        return {
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'author': self.author,
            'version': self.version,
            'colors': self.colors,
            'fonts': self.fonts,
            'spacing': self.spacing,
        }
    
    def __repr__(self):
        return f"<{self.__class__.__name__}: '{self.display_name}' v{self.version}>"
