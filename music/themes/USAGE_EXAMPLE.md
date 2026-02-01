# 🚀 Пример конвертации существующего шаблона

## Было (Hardcoded)

```django
{% extends 'music/base.html' %}
{% load static %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/steam-cards.css' %}">
<link rel="stylesheet" href="{% static 'css/steam-carousel.css' %}">
<link rel="stylesheet" href="{% static 'css/glass-liquid.css' %}">
{% endblock %}

{% block content %}
<!-- Featured Banner -->
<section class="max-w-[1920px] mx-auto mb-16" data-glass-context>
    <div class="steam-featured" data-track-id="{{ music_files.0.pk }}">
        <div class="steam-featured-bg">
            <img src="{{ music_files.0.cover_image.url }}" alt="...">
        </div>
        <div class="steam-featured-overlay"></div>
        <div class="steam-featured-content">
            <h1 class="steam-featured-title">{{ music_files.0.title }}</h1>
            <p class="steam-featured-artist">{{ music_files.0.artist.name }}</p>
            <!-- ... rest of featured banner ... -->
        </div>
    </div>
</section>

<!-- Carousel -->
<section class="steam-carousel-section">
    <div class="steam-carousel-header">
        <h2><i class="fas fa-clock"></i> Recently Added</h2>
    </div>
    <div class="steam-carousel-wrapper">
        <div class="steam-carousel">
            {% for track in music_files %}
            <div class="steam-carousel-item">
                <!-- hardcoded card markup -->
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<!-- Grid -->
<div class="steam-grid">
    {% for track in music_files %}
    <div class="steam-card" data-track-id="{{ track.pk }}">
        <!-- hardcoded card markup -->
    </div>
    {% endfor %}
</div>

{% endblock %}

{% block extra_js %}
<script src="{% static 'js/steam-carousel.js' %}"></script>
{% endblock %}
```

## 🎉 Стало (Theme-based)

```django
{% extends 'music/base.html' %}
{% load theme_tags %}

{% block extra_css %}
    {% theme_css %}
{% endblock %}

{% block content %}
<!-- Featured Banner -->
{% if music_files %}
    {% theme_featured track=music_files.0 %}
{% endif %}

<!-- Recently Added Carousel -->
{% theme_carousel tracks=music_files|slice:":12" title="Recently Added" icon="fas fa-clock" %}

<!-- Trending Carousel -->
{% theme_carousel tracks=music_files|slice:"6:18" title="Trending Now" icon="fas fa-fire" %}

<!-- All Tracks Grid -->
<section class="max-w-[1920px] mx-auto mb-20">
    <h2 class="text-3xl font-bold mb-8">
        <i class="fas fa-grip text-red-500"></i>
        All Tracks
    </h2>
    <div class="steam-grid">
        {% for track in music_files %}
            {% theme_card track %}
        {% endfor %}
    </div>
</section>

{% endblock %}

{% block extra_js %}
    {% theme_js %}
{% endblock %}
```

## ✨ Преимущества

1. **Меньше кода**: 150+ строк → 50 строк
2. **Легко поддерживать**: все изменения в одном месте
3. **Переиспользуемо**: компоненты для всех страниц
4. **Смена тем**: 1 строка кода

---

## 🔄 Theme Switcher View

```python
# music/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from music.themes import ThemeRegistry

def theme_switcher(request):
    """Theme selector page"""
    themes = ThemeRegistry.get_all_themes()
    active_theme = ThemeRegistry.get_active_theme()
    
    context = {
        'themes': themes,
        'active_theme': active_theme,
    }
    
    return render(request, 'music/theme_switcher.html', context)

def change_theme(request, theme_name):
    """Change active theme"""
    try:
        ThemeRegistry.set_active_theme(theme_name)
        theme = ThemeRegistry.get_theme(theme_name)
        messages.success(request, f'Theme changed to {theme.display_name}')
    except ValueError:
        messages.error(request, f'Theme "{theme_name}" not found')
    
    return redirect(request.META.get('HTTP_REFERER', 'music:index'))
```

```python
# music/urls.py

from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    # ... existing urls ...
    path('themes/', views.theme_switcher, name='theme_switcher'),
    path('themes/change/<str:theme_name>/', views.change_theme, name='change_theme'),
]
```

```django
{# music/templates/music/theme_switcher.html #}
{% extends 'music/base.html' %}
{% load theme_tags %}

{% block extra_css %}
{% theme_css %}
<style>
.theme-preview {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.3s ease;
}
.theme-preview:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.6);
}
.theme-preview.active {
    border: 3px solid #e31837;
}
</style>
{% endblock %}

{% block content %}
<div class="max-w-[1920px] mx-auto py-12">
    <h1 class="text-5xl font-black mb-4">
        <i class="fas fa-palette text-red-500"></i>
        Theme Selector
    </h1>
    <p class="text-white/60 text-lg mb-12">Choose your visual style</p>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {% for theme in themes %}
        <div class="theme-preview glass-layer-2 glass-radius-2xl p-6 {% if theme.name == active_theme.name %}active{% endif %}">
            <div class="flex items-start justify-between mb-4">
                <div>
                    <h3 class="text-2xl font-bold">{{ theme.display_name }}</h3>
                    <p class="text-sm text-white/40">v{{ theme.version }}</p>
                </div>
                {% if theme.name == active_theme.name %}
                <span class="px-3 py-1 bg-red-500 rounded-full text-xs font-bold">
                    Active
                </span>
                {% endif %}
            </div>
            
            <p class="text-white/70 mb-4">{{ theme.description }}</p>
            
            <div class="flex gap-2 mb-4">
                {% for color_name, color_value in theme.colors.items %}
                    {% if forloop.counter <= 5 %}
                    <div class="w-8 h-8 rounded-lg" 
                         style="background: {{ color_value }}" 
                         title="{{ color_name }}"></div>
                    {% endif %}
                {% endfor %}
            </div>
            
            <p class="text-xs text-white/40 mb-4">By {{ theme.author }}</p>
            
            {% if theme.name != active_theme.name %}
            <a href="{% url 'music:change_theme' theme.name %}" 
               class="glass-red-tint glass-radius-xl glass-pressable px-6 py-3 block text-center font-semibold">
                <i class="fas fa-check mr-2"></i>Activate
            </a>
            {% else %}
            <button disabled class="glass-layer-3 glass-radius-xl px-6 py-3 block text-center font-semibold w-full opacity-50 cursor-not-allowed">
                <i class="fas fa-check mr-2"></i>Active
            </button>
            {% endif %}
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

---

## 🔧 Конфигурация settings.py

```python
# music_stream/settings.py

# Default active theme (optional, can be set in apps.py)
ACTIVE_THEME = 'steam'  # or 'apple_glass' or 'spotify'

# Theme-specific settings (optional)
THEME_CONFIG = {
    'allow_user_switching': True,  # Позволить пользователям менять тему
    'cache_theme_assets': True,     # Кэширование CSS/JS
    'minify_assets': True,          # Минификация в production
}

# Add theme context processor (optional)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # ... existing processors ...
                'music.context_processors.theme_context',  # Добавьте это
            ],
        },
    },
]
```

```python
# music/context_processors.py (create this file)

from music.themes import ThemeRegistry

def theme_context(request):
    """Add theme to context for all templates"""
    return {
        'current_theme': ThemeRegistry.get_active_theme(),
        'all_themes': ThemeRegistry.get_all_themes(),
    }
```

---

## 🎯 Быстрый старт для нового проекта

1. **Скопируйте `music/themes/` в свой проект**
2. **Скопируйте `static/css/` и `static/js/`**
3. **Обновите `apps.py`** (см. выше)
4. **Используйте `{% load theme_tags %}`** в шаблонах
5. **Готово!** ✨

---

## 🔥 Продвинутое использование

### Per-User Themes (тема для каждого пользователя)

```python
# models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=50, default='steam')

# middleware.py
from music.themes import ThemeRegistry

class UserThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            profile = request.user.userprofile
            ThemeRegistry.set_active_theme(profile.theme)
        
        response = self.get_response(request)
        return response
```

### Dynamic Theme Generation

```python
# Generate theme from color palette
from music.themes.base import BaseTheme

def create_custom_theme(name, primary_color, secondary_color):
    class CustomTheme(BaseTheme):
        name = name
        display_name = f"Custom {name.title()}"
        colors = {
            'primary': primary_color,
            'secondary': secondary_color,
            # ... generate rest ...
        }
    
    ThemeRegistry.register_theme_class(CustomTheme)
    return CustomTheme
```

---

**🎉 Теперь у вас есть полноценный UI Framework!**
