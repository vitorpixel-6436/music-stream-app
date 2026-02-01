"""
Base Theme Class

All themes inherit from this.
"""

class BaseTheme:
    """Base theme with default templates and assets"""
    
    # Theme metadata
    name = 'base'
    display_name = 'Base Theme'
    description = 'Minimal base theme'
    author = 'Music Stream'
    version = '1.0.0'
    
    def get_static_css(self):
        """Return list of CSS files for this theme"""
        return []
    
    def get_static_js(self):
        """Return list of JS files for this theme"""
        return []
    
    def get_card_template(self):
        """Template path for music card component"""
        return 'music/components/card_base.html'
    
    def get_player_template(self):
        """Template path for player page"""
        return 'music/player.html'
    
    def get_index_template(self):
        """Template path for index/list page"""
        return 'music/index.html'
    
    def get_upload_template(self):
        """Template path for upload page"""
        return 'music/upload.html'
    
    def get_theme_config(self):
        """Additional theme-specific configuration"""
        return {
            'card_aspect_ratio': '3/4',
            'grid_columns': 'auto-fill',
            'animation_speed': 'normal',
        }
