# 🎨 Music Stream UI Framework

> Модульная система тем для быстрого развертывания музыкальных приложений

## 📚 Содержание

- [Введение](#введение)
- [Быстрый старт](#быстрый-старт)
- [Создание темы](#создание-темы)
- [Использование в шаблонах](#использование-в-шаблонах)
- [Компоненты](#компоненты)
- [API Reference](#api-reference)

---

## 🚀 Введение

UI Framework позволяет:
- ✅ Быстро разворачивать новые проекты с готовым UI
- ✅ Легко переключаться между темами
- ✅ Создавать кастомные темы без изменения основного кода
- ✅ Использовать компонентную архитектуру
- ✅ Расширять существующие темы

### Архитектура

```
music/themes/
├── base.py              # Базовые классы (BaseTheme, Component)
├── registry.py          # ThemeRegistry (управление темами)
├── configs/             # Конфигурации тем
│   ├── steam.py        # Steam Gaming Theme
│   ├── apple_glass.py  # Apple Glass Theme
│   └── spotify.py      # Spotify Minimal Theme
└── templatetags/        # Django template tags
    └── theme_tags.py
```

---

## ⚡ Быстрый старт

### 1. Регистрация тем (в `apps.py`)

```python
from django.apps import AppConfig

class MusicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'music'

    def ready(self):
        # Импортируем темы
        from music.themes import ThemeRegistry
        from music.themes.configs.steam import SteamTheme
        from music.themes.configs.apple_glass import AppleGlassTheme
        from music.themes.configs.spotify import SpotifyTheme
        
        # Регистрируем
        ThemeRegistry.register_theme_class(SteamTheme)
        ThemeRegistry.register_theme_class(AppleGlassTheme)
        ThemeRegistry.register_theme_class(SpotifyTheme)
        
        # Устанавливаем активную тему
        ThemeRegistry.set_active_theme('steam')
```

### 2. Настройка `settings.py`

```python
# Активная тема (опционально, можно задать в apps.py)
ACTIVE_THEME = 'steam'

# Добавить в INSTALLED_APPS (если ещё нет)
INSTALLED_APPS = [
    # ...
    'music',
]
```

### 3. Использование в шаблонах

```django
{% load theme_tags %}
<!DOCTYPE html>
<html>
<head>
    <title>Music Stream</title>
    {% theme_css %}
</head>
<body>
    {# Featured banner #}
    {% theme_featured track=featured_track %}
    
    {# Carousel #}
    {% theme_carousel tracks=recent_tracks title="Recently Added" icon="fas fa-clock" %}
    
    {# Grid of cards #}
    <div class="steam-grid">
        {% for track in all_tracks %}
            {% theme_card track %}
        {% endfor %}
    </div>
    
    {% theme_js %}
</body>
</html>
```

---

## 🎨 Создание темы

### Шаг 1: Создайте класс темы

```python
# music/themes/configs/my_theme.py

from music.themes.base import BaseTheme, Component

class MyTheme(BaseTheme):
    name = 'my_theme'
    display_name = 'My Awesome Theme'
    description = 'Custom theme for my project'
    author = 'Your Name'
    version = '1.0.0'
    
    # Цвета
    colors = {
        'primary': '#ff6b6b',
        'secondary': '#4ecdc4',
        'background': '#1a1a2e',
        'text': '#eee',
    }
    
    # Шрифты
    fonts = {
        'primary': 'Roboto, sans-serif',
        'heading': 'Montserrat, sans-serif',
    }
    
    # Отступы
    spacing = {
        'sm': '0.5rem',
        'md': '1rem',
        'lg': '2rem',
    }
    
    def _register_components(self):
        # Регистрируем компоненты
        self.register_component(Component(
            name='card',
            template='themes/my_theme/card.html',
            css=['themes/my_theme/card.css'],
            js=['themes/my_theme/card.js']
        ))
    
    def get_css_files(self):
        return [
            'themes/my_theme/style.css',
        ]
    
    def get_js_files(self):
        return [
            'themes/my_theme/main.js',
        ]
```

### Шаг 2: Зарегистрируйте тему

```python
# В apps.py
from music.themes.configs.my_theme import MyTheme
ThemeRegistry.register_theme_class(MyTheme)
```

### Шаг 3: Создайте CSS/JS файлы

```css
/* static/themes/my_theme/style.css */
:root {
    --color-primary: #ff6b6b;
    --color-secondary: #4ecdc4;
}

.theme-card {
    background: var(--color-primary);
    border-radius: 12px;
    padding: 1rem;
}
```

---

## 🧩 Компоненты

### Card (Карточка трека)

```django
{% theme_card track %}
```

**Параметры:**
- `track` - объект MusicFile

### Carousel (Карусель)

```django
{% theme_carousel tracks=tracks title="Title" icon="fas fa-music" %}
```

**Параметры:**
- `tracks` - список треков
- `title` - заголовок (опционально)
- `icon` - иконка FontAwesome (опционально)

### Featured (Featured баннер)

```django
{% theme_featured track=track %}
```

**Параметры:**
- `track` - объект MusicFile

---

## 📖 API Reference

### ThemeRegistry

```python
from music.themes import ThemeRegistry

# Получить активную тему
theme = ThemeRegistry.get_active_theme()

# Установить активную тему
ThemeRegistry.set_active_theme('steam')

# Получить все темы
themes = ThemeRegistry.get_all_themes()

# Получить конкретную тему
steam_theme = ThemeRegistry.get_theme('steam')
```

### BaseTheme

```python
# Получить CSS файлы
css_files = theme.get_css_files()

# Получить JS файлы
js_files = theme.get_js_files()

# Получить компонент
card_component = theme.get_component('card')

# Получить конфигурацию
config = theme.get_config()
print(config['colors']['primary'])  # #e31837
```

### Template Tags

```django
{# Загрузка CSS/JS #}
{% theme_css %}
{% theme_js %}

{# Загрузка CSS/JS для компонента #}
{% component_css 'card' %}
{% component_js 'carousel' %}

{# Рендеринг компонентов #}
{% theme_card track %}
{% theme_carousel tracks title="Title" %}
{% theme_featured track %}

{# Получение конфига темы #}
{% get_theme_config as config %}
{{ config.colors.primary }}

{# Получение темы #}
{% get_theme as theme %}
{{ theme.display_name }}

{# Список всех тем #}
{% get_all_themes as themes %}
{% for theme in themes %}
    {{ theme.display_name }}
{% endfor %}

{# Фильтр для цветов #}
<div style="background: {{ 'primary'|theme_color }}">
```

---

## 🎯 Примеры использования

### Пример 1: Простая страница с карточками

```django
{% extends 'base.html' %}
{% load theme_tags %}

{% block extra_css %}
    {% theme_css %}
{% endblock %}

{% block content %}
<div class="container">
    <h1>All Tracks</h1>
    <div class="steam-grid">
        {% for track in tracks %}
            {% theme_card track %}
        {% endfor %}
    </div>
</div>
{% endblock %}

{% block extra_js %}
    {% theme_js %}
{% endblock %}
```

### Пример 2: Домашняя страница с каруселями

```django
{% extends 'base.html' %}
{% load theme_tags %}

{% block content %}
{# Featured banner #}
{% if featured_track %}
    {% theme_featured track=featured_track %}
{% endif %}

{# Recently added #}
{% theme_carousel tracks=recent_tracks title="Recently Added" icon="fas fa-clock" %}

{# Popular #}
{% theme_carousel tracks=popular_tracks title="Popular" icon="fas fa-fire" %}

{# All tracks grid #}
<section class="all-tracks">
    <h2>All Music</h2>
    <div class="steam-grid">
        {% for track in all_tracks %}
            {% theme_card track %}
        {% endfor %}
    </div>
</section>
{% endblock %}
```

### Пример 3: Динамическая смена темы

```python
# views.py
from django.shortcuts import render, redirect
from music.themes import ThemeRegistry

def change_theme(request, theme_name):
    """Switch active theme"""
    try:
        ThemeRegistry.set_active_theme(theme_name)
        return redirect('music:index')
    except ValueError:
        return redirect('music:index')

def theme_selector(request):
    """Show theme selector page"""
    themes = ThemeRegistry.get_all_themes()
    active_theme = ThemeRegistry.get_active_theme()
    
    return render(request, 'themes/selector.html', {
        'themes': themes,
        'active_theme': active_theme,
    })
```

```django
{# themes/selector.html #}
{% for theme in themes %}
<div class="theme-preview">
    <h3>{{ theme.display_name }}</h3>
    <p>{{ theme.description }}</p>
    <a href="{% url 'music:change_theme' theme.name %}">Activate</a>
</div>
{% endfor %}
```

---

## 🔧 Расширение существующих тем

```python
from music.themes.configs.steam import SteamTheme

class MySteamTheme(SteamTheme):
    name = 'my_steam'
    display_name = 'My Custom Steam'
    
    # Переопределяем цвета
    colors = {
        **SteamTheme.colors,
        'primary': '#00ff00',  # Зелёный вместо красного
    }
    
    def get_css_files(self):
        # Добавляем свой CSS к базовому
        return super().get_css_files() + [
            'themes/my_steam/custom.css',
        ]
```

---

## 💡 Best Practices

1. **Используйте компонентную архитектуру** - создавайте переиспользуемые компоненты
2. **Следуйте naming conventions** - `theme_name`, `ComponentName`
3. **Документируйте цвета** - добавляйте комментарии к палитре
4. **Тестируйте на разных разрешениях** - responsive design обязателен
5. **Используйте CSS variables** - для легкой кастомизации
6. **Минифицируйте CSS/JS** - в production

---

## 🐛 Troubleshooting

### Тема не загружается

```python
# Проверьте регистрацию
from music.themes import ThemeRegistry
print(ThemeRegistry.get_theme_names())  # Список зарегистрированных тем
```

### CSS/JS не подключаются

```python
# Проверьте пути
theme = ThemeRegistry.get_active_theme()
print(theme.get_css_files())
print(theme.get_js_files())
```

### Компонент не рендерится

```python
# Проверьте компоненты
theme = ThemeRegistry.get_active_theme()
print(theme.get_all_components())
```

---

## 📄 License

MIT License - свободно используйте в своих проектах!

---

## 🤝 Contributing

Приветствуются пулл-реквесты с новыми темами!

1. Fork проект
2. Создайте ветку (`git checkout -b feature/new-theme`)
3. Commit изменения (`git commit -am 'Add new theme'`)
4. Push в ветку (`git push origin feature/new-theme`)
5. Создайте Pull Request

---

**Made with ❤️ by Music Stream Team**
