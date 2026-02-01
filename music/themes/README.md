# 🎨 Music Stream UI Theme System

Модульная система тем для быстрого создания красивых интерфейсов.

## 🚀 Быстрый старт

### Использование существующей темы

```python
# settings.py
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'music.context_processors.theme_context',  # Добавь это
            ],
        },
    },
]
```

```python
# apps.py или __init__.py
from music.themes import registry
from music.themes.steam import SteamTheme

# Регистрируем темы
registry.register(SteamTheme)
registry.set_active_theme('steam')
```

### В шаблонах

```django
{% load theme_tags %}

<!DOCTYPE html>
<html>
<head>
    {% load_theme_assets %}  <!-- Автоматически загружает CSS/JS темы -->
</head>
<body>
    {% for track in tracks %}
        {% include theme.get_card_template with track=track %}
    {% endfor %}
</body>
</html>
```

---

## 🎯 Создание новой темы

### Шаг 1: Создай класс темы

```python
# music/themes/my_theme.py

from .base import BaseTheme

class MyTheme(BaseTheme):
    name = 'mytheme'
    display_name = 'My Awesome Theme'
    description = 'Clean minimalist design'
    
    def get_static_css(self):
        return ['css/mytheme.css']
    
    def get_theme_config(self):
        return {
            'card_aspect_ratio': '1/1',  # Квадратные карточки
            'animation_speed': 'slow',
        }
```

### Шаг 2: Регистрируй тему

```python
from music.themes import registry
from music.themes.my_theme import MyTheme

registry.register(MyTheme)
registry.set_active_theme('mytheme')
```

### Шаг 3: Создай стили

```css
/* static/css/mytheme.css */
.music-card {
    border-radius: 8px;
    background: white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
```

---

## 📦 Структура темы

```
music/
├── themes/
│   ├── __init__.py          # Auto-registration
│   ├── base.py              # BaseTheme class
│   ├── registry.py          # Theme registry
│   ├── steam.py             # Steam theme
│   └── your_theme.py        # Your theme
├── templates/
│   └── music/
│       ├── components/
│       │   └── card_base.html
│       └── themes/
│           └── steam/
│               └── card.html
└── static/
    ├── css/
    │   ├── steam-cards.css
    │   └── your-theme.css
    └── js/
        └── steam-carousel.js
```

---

## 🎨 Доступные методы BaseTheme

| Метод | Описание |
|-------|----------|
| `get_static_css()` | Список CSS файлов |
| `get_static_js()` | Список JS файлов |
| `get_card_template()` | Шаблон карточки трека |
| `get_player_template()` | Шаблон плеера |
| `get_index_template()` | Шаблон главной страницы |
| `get_theme_config()` | Конфигурация темы (dict) |

---

## 🔧 Конфигурация темы

Все темы могут определять кастомные настройки:

```python
def get_theme_config(self):
    return {
        'card_aspect_ratio': '3/4',
        'grid_columns': 'auto-fill',
        'animation_speed': 'fast',
        'glass_effect': True,
        'carousel_enabled': True,
        'primary_color': '#e31837',
    }
```

Доступ в шаблонах:

```django
{% theme_config 'primary_color' '#000000' %}
```

---

## 🎯 Примеры тем

### Steam Theme (включена)
- Игровой дизайн в стиле Steam
- Glass morphism эффекты
- Карусели и featured баннеры

### Minimal Theme (пример)
```python
class MinimalTheme(BaseTheme):
    name = 'minimal'
    display_name = 'Minimal Clean'
    
    def get_static_css(self):
        return ['css/minimal.css']
    
    def get_theme_config(self):
        return {
            'card_aspect_ratio': '1/1',
            'animation_speed': 'none',
        }
```

---

## 🚀 Преимущества

✅ **Быстрое развертывание** - новая тема за 5 минут  
✅ **Нет дублирования** - переиспользуй компоненты  
✅ **Гибкость** - переопредели любой метод  
✅ **Легкое переключение** - одна строка кода  
✅ **Type-safe** - все через базовый класс  

---

## 📝 TODO / Roadmap

- [ ] Theme marketplace/gallery
- [ ] Live theme preview
- [ ] Theme settings UI
- [ ] Export/import themes
- [ ] Theme inheritance
- [ ] Component library documentation
