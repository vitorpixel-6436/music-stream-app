# 🎨 Steam UI Framework

A modular, reusable UI component library inspired by Steam's design language with glass morphism effects.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Django](https://img.shields.io/badge/django-4.0%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

- 🎭 **Glass Morphism Effects** - Multi-layered frosted glass components
- 🎮 **Steam-Inspired Design** - Gaming-oriented dark theme
- 📦 **Modular Components** - Card, Carousel, Featured Banner, etc.
- 🔧 **Highly Customizable** - Configuration system and theming
- 🚀 **Easy Integration** - Django template tags and Python API
- 📱 **Responsive** - Mobile-first design
- ⚡ **Performance** - Optimized animations and lazy loading

---

## 📦 Installation

### Option 1: From repository

```bash
pip install git+https://github.com/vitorpixel-6436/music-stream-app.git
```

### Option 2: Local development

```bash
cd /path/to/music-stream-app
pip install -e .
```

---

## 🚀 Quick Start

### 1. Add to INSTALLED_APPS

```python
# settings.py
INSTALLED_APPS = [
    ...
    'steam_ui',  # Add this
]
```

### 2. Configure static files

```python
# settings.py
STATICFILES_DIRS = [
    ...
    BASE_DIR / 'steam_ui' / 'static',
]
```

### 3. Use in templates

```django
{% load steam_ui %}

<!DOCTYPE html>
<html>
<head>
    {% steam_css %}  <!-- Load all CSS -->
</head>
<body class="bg-gradient-to-br from-black via-gray-900 to-black min-h-screen">

    <!-- Featured Banner -->
    {% steam_featured featured_track %}
    
    <!-- Carousel -->
    {% steam_carousel recent_tracks title="Recently Added" icon="fa-clock" %}
    
    <!-- Individual Cards -->
    <div class="grid grid-cols-4 gap-8">
        {% for track in tracks %}
            {% steam_card track %}
        {% endfor %}
    </div>
    
    {% steam_js %}  <!-- Load all JS -->
</body>
</html>
```

---

## 📚 Components

### 🃏 Card

Steam-style track card with hover effects.

**Template Tag:**
```django
{% steam_card track %}
{% steam_card track show_actions=False %}
{% steam_card track size='large' %}
```

**Python API:**
```python
from steam_ui import Card

card = Card(show_actions=True, size='normal')
html = card.render(track=track_object)
```

**Parameters:**
- `track`: Track object (required)
- `show_actions`: Show action buttons (default: `True`)
- `size`: Card size - `'normal'`, `'large'`, `'small'` (default: `'normal'`)

---

### 🎠 Carousel

Horizontal scrolling carousel with navigation.

**Template Tag:**
```django
{% steam_carousel tracks %}
{% steam_carousel tracks title="Popular" icon="fa-fire" %}
{% steam_carousel tracks show_navigation=False %}
```

**Python API:**
```python
from steam_ui import Carousel

carousel = Carousel(title="Recently Added", icon="fa-clock")
html = carousel.render(tracks=track_list)
```

**Parameters:**
- `tracks`: List of track objects (required)
- `title`: Section title (default: `"Tracks"`)
- `icon`: FontAwesome icon class (default: `"fa-music"`)
- `show_navigation`: Show arrow buttons (default: `True`)

---

### 🎯 Featured Banner

Hero section with large cover image.

**Template Tag:**
```django
{% steam_featured track %}
{% steam_featured track cta_primary="Listen Now" %}
{% steam_featured track show_description=False %}
```

**Python API:**
```python
from steam_ui import FeaturedBanner

banner = FeaturedBanner(cta_primary="Play Now")
html = banner.render(track=featured_track)
```

**Parameters:**
- `track`: Featured track object (required)
- `show_description`: Show description text (default: `True`)
- `cta_primary`: Primary button text (default: `"Play Now"`)
- `cta_secondary`: Secondary button text (default: `"Download"`)

---

### 🏷️ Category Pills

Filter pills for categories.

**Template Tag:**
```django
{% steam_category_pills categories %}
{% steam_category_pills categories active='recent' %}
```

**Python API:**
```python
from steam_ui import CategoryPills

pills = CategoryPills()
html = pills.render(categories=category_list, active='all')
```

---

## ⚙️ Configuration

### Global Settings

```python
# your_app/apps.py or settings.py
from steam_ui.config import config

config.update(
    # Static files
    STATIC_URL='/static/steam_ui/',
    USE_CDN=True,
    CDN_URL='https://cdn.example.com',
    
    # Features
    ENABLE_ANIMATIONS=True,
    ENABLE_GLASS_EFFECTS=True,
    ENABLE_AUTO_PLAY=False,
    
    # Performance
    LAZY_LOAD_IMAGES=True,
    PRELOAD_COVERS=6,
    
    # Theme colors
    PRIMARY_COLOR='#e31837',  # Steam red
    GLASS_BLUR='20px',
    GLASS_OPACITY=0.08,
)
```

### Access config in templates

```django
{{ 'PRIMARY_COLOR'|steam_config }}
{{ 'ENABLE_ANIMATIONS'|steam_config }}
```

---

## 🎨 CSS Modules

### Load specific CSS

```django
{% steam_css 'glass-liquid' 'steam-cards' %}
```

### Available modules:

- `glass-liquid.css` - Glass morphism effects
- `glass-dynamics.css` - Dynamic glass animations
- `steam-cards.css` - Card components
- `steam-carousel.css` - Carousel components
- `msi-gaming.css` - Gaming accents
- `spotify-minimal.css` - Minimal theme

---

## 🔧 Advanced Usage

### Custom Component

```python
from steam_ui.components import BaseComponent

class MyCustomCard(BaseComponent):
    template_name = 'my_app/custom_card.html'
    
    def __init__(self, border_color='#e31837', **kwargs):
        super().__init__(**kwargs)
        self.border_color = border_color
    
    def get_context(self, **kwargs):
        context = super().get_context(**kwargs)
        context['border_color'] = self.border_color
        return context

# Usage
card = MyCustomCard(border_color='#00ff00')
html = card.render(item=my_item)
```

### Render in views

```python
from django.shortcuts import render
from steam_ui import Card, Carousel

def index(request):
    tracks = Track.objects.all()
    
    # Render components
    carousel_html = Carousel(title="All Tracks").render(tracks=tracks)
    
    return render(request, 'index.html', {
        'carousel_html': carousel_html,
    })
```

---

## 🎯 Examples

### Music Player Page

```django
{% load steam_ui %}

{% steam_css %}

<main class="container mx-auto px-4 py-8">
    <!-- Hero -->
    {% steam_featured featured_track %}
    
    <!-- Category Filter -->
    {% steam_category_pills categories %}
    
    <!-- Recently Added -->
    {% steam_carousel recent_tracks title="Recently Added" icon="fa-clock" %}
    
    <!-- Trending -->
    {% steam_carousel trending_tracks title="Trending" icon="fa-fire" %}
    
    <!-- All Tracks Grid -->
    <section class="mt-16">
        <h2 class="text-3xl font-bold mb-8">All Tracks</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-8">
            {% for track in all_tracks %}
                {% steam_card track %}
            {% endfor %}
        </div>
    </section>
</main>

{% steam_js %}
```

---

## 📖 Track Object Requirements

Your track model should have these attributes:

```python
class Track(models.Model):
    title = models.CharField(max_length=200)  # Required
    artist = models.ForeignKey(Artist)         # Required (.name)
    cover_image = models.ImageField()          # Optional
    duration = models.FloatField()             # Optional
    pk = models.UUIDField()                    # Required for URLs
```

---

## 🛠️ Development

### Project Structure

```
steam_ui/
├── __init__.py              # Package init
├── components.py            # Component classes
├── config.py               # Configuration
├── templatetags/
│   ├── __init__.py
│   └── steam_ui.py         # Template tags
├── templates/
│   └── steam_ui/
│       ├── card.html
│       ├── carousel.html
│       └── featured.html
└── static/
    └── steam_ui/
        ├── css/            # Stylesheets
        └── js/             # JavaScript
```

### Run tests

```bash
pytest
```

---

## 📄 License

MIT License - feel free to use in your projects!

---

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

---

## 🔗 Links

- [GitHub Repository](https://github.com/vitorpixel-6436/music-stream-app)
- [Issue Tracker](https://github.com/vitorpixel-6436/music-stream-app/issues)

---

**Made with ❤️ by vitorpixel-6436**
