# 🎨 Steam UI Framework - Usage Examples

## 📚 Quick Reference

### Template Tags

```django
{% load steam_ui %}

{# Load CSS/JS #}
{% steam_css %}  <!-- All CSS -->
{% steam_css 'glass-liquid' 'steam-cards' %}  <!-- Specific modules -->
{% steam_js %}  <!-- All JS -->

{# Components #}
{% steam_card track %}
{% steam_carousel tracks title="Recent" icon="fa-clock" %}
{% steam_featured featured_track %}
{% steam_category_pills categories active='all' %}
```

---

## 🎯 Complete Page Example

### `music/templates/music/index.html`

```django
{% extends 'music/base.html' %}
{% load steam_ui %}

{% block title %}Music Library{% endblock %}

{% block extra_css %}
{% steam_css %}
{% endblock %}

{% block content %}

<!-- Featured Banner -->
{% if music_files %}
{% steam_featured music_files.0 %}
{% endif %}

<!-- Category Pills -->
{% steam_category_pills categories %}

<!-- Recently Added Carousel -->
{% steam_carousel music_files|slice:":12" title="Recently Added" icon="fa-clock" %}

<!-- Trending Carousel -->
{% steam_carousel music_files|slice:"6:18" title="Trending Now" icon="fa-fire" %}

<!-- All Tracks Grid -->
<section class="max-w-[1920px] mx-auto mb-20">
    <h2 class="text-3xl font-bold mb-8">
        <i class="fas fa-grip text-red-500 mr-3"></i>
        All Tracks
    </h2>
    <div class="steam-grid">
        {% for track in music_files %}
            {% steam_card track %}
        {% endfor %}
    </div>
</section>

{% endblock %}

{% block extra_js %}
{% steam_js %}
{% endblock %}
```

---

## 🐍 Python API Examples

### In Views

```python
from django.shortcuts import render
from steam_ui import Card, Carousel, FeaturedBanner
from .models import Track

def index(request):
    tracks = Track.objects.all()[:20]
    featured = Track.objects.first()
    
    # Render components in Python
    carousel_html = Carousel(
        title="Top Tracks",
        icon="fa-fire"
    ).render(tracks=tracks[:10])
    
    featured_html = FeaturedBanner(
        cta_primary="Listen Now",
        cta_secondary="Add to Library"
    ).render(track=featured)
    
    return render(request, 'index.html', {
        'carousel_html': carousel_html,
        'featured_html': featured_html,
        'tracks': tracks,
    })
```

### Custom Component

```python
from steam_ui.components import BaseComponent

class AlbumCard(BaseComponent):
    template_name = 'myapp/album_card.html'
    
    def __init__(self, show_tracks=True, **kwargs):
        super().__init__(**kwargs)
        self.show_tracks = show_tracks
    
    def get_context(self, **kwargs):
        context = super().get_context(**kwargs)
        context['show_tracks'] = self.show_tracks
        return context

# Usage
album_card = AlbumCard(show_tracks=True)
html = album_card.render(album=album_obj)
```

---

## ⚙️ Configuration

### In `settings.py` or `apps.py`

```python
from steam_ui.config import config

# Customize colors
config.update(
    PRIMARY_COLOR='#ff0066',  # Custom accent color
    GLASS_BLUR='30px',        # Stronger blur
    GLASS_OPACITY=0.12,       # More visible glass
)

# Performance settings
config.update(
    LAZY_LOAD_IMAGES=True,
    PRELOAD_COVERS=6,
    ENABLE_ANIMATIONS=True,
)

# CDN support
config.update(
    USE_CDN=True,
    CDN_URL='https://cdn.example.com',
)
```

---

## 🔄 Migration Guide

### Before (Hardcoded)

```django
<!-- Old way -->
<link rel="stylesheet" href="{% static 'css/steam-cards.css' %}">

<div class="steam-card" data-track-id="{{ track.pk }}">
    <div class="steam-card-cover">
        <img src="{{ track.cover_image.url }}" alt="{{ track.title }}">
    </div>
    <!-- ... lots of HTML ... -->
</div>

<script src="{% static 'js/steam-carousel.js' %}"></script>
```

### After (Steam UI Framework)

```django
<!-- New way -->
{% load steam_ui %}
{% steam_css %}

{% steam_card track %}

{% steam_js %}
```

**Benefits:**
- ✅ 90% less code
- ✅ Consistent styling
- ✅ Easy to update globally
- ✅ Reusable across projects

---

## 🎨 Component Customization

### Card Variants

```django
<!-- Normal card -->
{% steam_card track %}

<!-- Large card -->
{% steam_card track size='large' %}

<!-- Without actions -->
{% steam_card track show_actions=False %}

<!-- Small card -->
{% steam_card track size='small' %}
```

### Carousel Options

```django
<!-- Basic carousel -->
{% steam_carousel tracks %}

<!-- Custom title and icon -->
{% steam_carousel tracks title="My Playlist" icon="fa-heart" %}

<!-- Without navigation -->
{% steam_carousel tracks show_navigation=False %}
```

### Featured Banner

```django
<!-- Default -->
{% steam_featured track %}

<!-- Custom buttons -->
{% steam_featured track cta_primary="Stream" cta_secondary="Buy" %}

<!-- Without description -->
{% steam_featured track show_description=False %}
```

---

## 🧩 Combining Components

```django
{% load steam_ui %}

<div class="container mx-auto">
    <!-- Hero section -->
    {% steam_featured featured_track %}
    
    <!-- Filter pills -->
    {% steam_category_pills categories active='all' %}
    
    <!-- Multiple carousels -->
    {% steam_carousel recent_tracks title="Just Added" icon="fa-clock" %}
    {% steam_carousel popular_tracks title="Popular" icon="fa-fire" %}
    {% steam_carousel your_tracks title="Your Library" icon="fa-user" %}
    
    <!-- Grid of cards -->
    <div class="steam-grid mt-16">
        {% for track in all_tracks %}
            {% steam_card track %}
        {% endfor %}
    </div>
</div>
```

---

## 🚀 Use in Other Projects

### 1. Install the package

```bash
pip install git+https://github.com/vitorpixel-6436/music-stream-app.git
```

### 2. Add to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    'steam_ui',
]
```

### 3. Configure templates and static

```python
TEMPLATES = [{
    'DIRS': [BASE_DIR / 'steam_ui' / 'templates'],
    ...
}]

STATICFILES_DIRS = [
    BASE_DIR / 'steam_ui' / 'static',
]
```

### 4. Use in templates

```django
{% load steam_ui %}
{% steam_css %}

{% steam_card your_object %}

{% steam_js %}
```

---

## 📝 Track Model Requirements

Your model should have these fields:

```python
class Track(models.Model):
    title = models.CharField(max_length=200)     # Required
    artist = models.ForeignKey(Artist)            # Required (with .name)
    cover_image = models.ImageField()             # Optional
    duration = models.FloatField()                # Optional
    pk = models.UUIDField(primary_key=True)      # Required
```

Or adapt the template to your model structure.

---

## 🎯 Best Practices

1. **Use template tags** instead of hardcoding HTML
2. **Customize via config** rather than modifying CSS directly
3. **Create custom components** for app-specific needs
4. **Keep components small** and focused on one thing
5. **Use Python API** when you need programmatic control

---

## 🔗 More Info

- [Full Documentation](steam_ui/README.md)
- [Component Reference](steam_ui/components.py)
- [Template Tags](steam_ui/templatetags/steam_ui.py)
- [Configuration](steam_ui/config.py)
