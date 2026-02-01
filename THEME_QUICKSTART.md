# 🎨 Theme System - Быстрый старт

## 🚀 Создать новую тему за 5 минут

### 1️⃣ Создай класс темы

```python
# music/themes/my_theme.py

from .base import BaseTheme

class MyTheme(BaseTheme):
    name = 'mytheme'
    display_name = 'Моя Тема'
    description = 'Крутой дизайн'
    
    def get_static_css(self):
        return ['css/mytheme.css']
```

### 2️⃣ Создай стили

```css
/* music/static/css/mytheme.css */

.music-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 16px;
    color: white;
}

.music-card:hover {
    transform: scale(1.05);
}
```

### 3️⃣ Зарегистрируй

```python
# music/apps.py

from music.themes.my_theme import MyTheme

def ready(self):
    from music.themes import registry
    registry.register(MyTheme)
    registry.set_active_theme('mytheme')  # Активируй
```

### ✅ Готово!

---

## 🎯 Примеры использования

### Переключение тем в runtime

```python
from music.themes import registry

# Посмотреть все темы
themes = registry.list_themes()
for theme in themes:
    print(f"{theme['name']}: {theme['display_name']}")

# Переключиться
registry.set_active_theme('minimal')
```

### Использование в шаблонах

```django
{% load theme_tags %}

<!DOCTYPE html>
<html>
<head>
    <title>Music App</title>
    {% load_theme_assets %}  <!-- Авто-загрузка CSS/JS -->
</head>
<body>
    <div class="container">
        {% for track in tracks %}
            {% include theme.get_card_template with track=track %}
        {% endfor %}
    </div>
</body>
</html>
```

### Доступ к конфигу

```django
<div style="aspect-ratio: {% theme_config 'card_aspect_ratio' '1/1' %}">
    <!-- Контент -->
</div>
```

---

## 📦 Доступные темы

### Steam Theme (`steam`)
- Игровой дизайн
- Glass morphism
- Карусели и анимации
- Featured баннеры

```python
registry.set_active_theme('steam')
```

### Minimal Theme (`minimal`)
- Минималистичный
- Быстрый
- Легкий в кастомизации
- Dark mode поддержка

```python
registry.set_active_theme('minimal')
```

---

## 🛠️ Продвинутое использование

### Переопределение компонентов

```python
class CustomTheme(BaseTheme):
    name = 'custom'
    
    def get_card_template(self):
        return 'my_app/custom_card.html'  # Свой шаблон
    
    def get_player_template(self):
        return 'my_app/custom_player.html'
```

### Динамическая конфигурация

```python
class AdaptiveTheme(BaseTheme):
    def get_theme_config(self):
        # Можно делать логику
        from django.conf import settings
        
        return {
            'primary_color': settings.BRAND_COLOR,
            'card_size': 'large' if settings.DEBUG else 'normal',
        }
```

### JS интеграция

```python
class InteractiveTheme(BaseTheme):
    def get_static_js(self):
        return [
            'js/my-theme-animations.js',
            'js/my-theme-interactions.js',
        ]
```

---

## 📝 Best Practices

1. **Не hardcode** - Используй `get_theme_config()`
2. **Reuse компоненты** - Наследуй `BaseTheme`
3. **Минимальный CSS** - Только что нужно для темы
4. **Документируй** - Docstrings в классах
5. **Тестируй** - Проверяй на разных разрешениях

---

## 👥 Community Themes

Хочешь поделиться своей темой? Отправь PR!

### Формат:
```python
class YourTheme(BaseTheme):
    name = 'yourtheme'
    display_name = 'Your Theme'
    description = 'Amazing design'
    author = 'Your Name'
    version = '1.0.0'
```
