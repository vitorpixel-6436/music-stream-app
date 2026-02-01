# 🛠️ Установка Theme System

## Шаг 1: Обнови `config/settings.py`

### Добавь context processor:

```python
# config/settings.py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                # Добавь эту строку ⬇️
                'music.context_processors.theme_context',
            ],
        },
    },
]
```

## Шаг 2: Проверь `music/apps.py`

Убедись что есть `ready()` метод:

```python
# music/apps.py

from django.apps import AppConfig

class MusicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'music'

    def ready(self):
        """Initialize themes when app loads"""
        from music.themes import registry
        from music.themes.steam import SteamTheme
        from music.themes.minimal import MinimalTheme
        
        # Register all themes
        registry.register(SteamTheme)
        registry.register(MinimalTheme)
        
        # Set default theme
        registry.set_active_theme('steam')
```

## Шаг 3: Создай templatetags директорию

```bash
mkdir -p music/templatetags
touch music/templatetags/__init__.py
```

Файл `music/templatetags/theme_tags.py` уже создан.

## Шаг 4: Перезапусти сервер

```bash
# Останови
Ctrl+C

# Запусти заново
python manage.py runserver
```

---

## ✅ Проверка установки

### В Django shell:

```bash
python manage.py shell
```

```python
>>> from music.themes import registry
>>> themes = registry.list_themes()
>>> for t in themes:
...     print(f"{t['name']}: {t['display_name']}")

steam: Steam Gaming
minimal: Minimal Clean

>>> # Переключение темы
>>> registry.set_active_theme('minimal')
True

>>> active = registry.get_active_theme()
>>> print(active.display_name)
Minimal Clean
```

---

## 🐞 Troubleshooting

### Ошибка: `ModuleNotFoundError: No module named 'music.themes'`

**Решение:**
```bash
# Убедись что созданы все файлы:
ls -la music/themes/

# Должны быть:
# __init__.py
# base.py
# registry.py
# steam.py
# minimal.py
```

### Ошибка: `TemplateDoesNotExist: music/themes/steam/card.html`

**Решение:**
```bash
# Создай директорию
mkdir -p music/templates/music/themes/steam/

# Файл уже должен быть создан в music/themes/templates/steam/card.html
# Перемести его в правильное место
```

### CSS не загружается

**Решение:**
```bash
# Собери статику
python manage.py collectstatic --noinput

# Очисти кэш браузера
# Ctrl+Shift+R (или Cmd+Shift+R на Mac)
```

---

## 🔧 Расширенные настройки

### Выбор темы через переменную окружения:

```python
# config/settings.py

import os

# Theme configuration
DEFAULT_THEME = os.getenv('MUSIC_THEME', 'steam')
```

```python
# music/apps.py

def ready(self):
    from django.conf import settings
    from music.themes import registry
    from music.themes.steam import SteamTheme
    from music.themes.minimal import MinimalTheme
    
    registry.register(SteamTheme)
    registry.register(MinimalTheme)
    
    # Используй настройку из settings
    registry.set_active_theme(settings.DEFAULT_THEME)
```

### Тема на основе пользователя:

```python
# music/middleware.py

class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from music.themes import registry
        
        # Получи тему из профиля или cookie
        theme_name = request.COOKIES.get('theme', 'steam')
        registry.set_active_theme(theme_name)
        
        response = self.get_response(request)
        return response
```

```python
# config/settings.py

MIDDLEWARE = [
    # ... other middleware
    'music.middleware.ThemeMiddleware',
]
```

---

## 🚀 Готово!

Теперь можно:
- ✅ Использовать существующие темы
- ✅ Создавать новые темы
- ✅ Переключать темы налету

См. **THEME_QUICKSTART.md** для примеров использования!
