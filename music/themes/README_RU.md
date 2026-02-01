# 🎨 Система Тем Music Stream

Модульная система UI-тем для **быстрого развертывания** новых интерфейсов без дублирования кода.

## 🚀 Зачем это нужно?

### До (hardcoded UI):
```python
# Каждый проект - копи-паста всего CSS/JS
# Менять дизайн = переписывать половину кода
# Поддерживать несколько дизайнов = кошмар
```

### После (Theme System):
```python
# Создал новую тему за 5 минут
registry.register(MyTheme)
registry.set_active_theme('mytheme')

# Переключился - готово!
```

---

## ✨ Преимущества

| Что | Как |
|-----|-----|
| 🚀 **Быстрое развертывание** | Новый UI за минуты, не часы |
| 📦 **Нет дублирования** | Переиспользуй компоненты |
| 🎯 **Гибкость** | Переопредели только что нужно |
| ⚡ **Легкое переключение** | Одна строка кода |
| 🛡️ **Type-safe** | Всё через базовый класс |

---

## 📚 Документация

- 🛠️ [**INSTALL_THEMES.md**](../../INSTALL_THEMES.md) - Установка системы
- 🚀 [**THEME_QUICKSTART.md**](../../THEME_QUICKSTART.md) - Быстрый старт
- 📝 [**README.md**](README.md) - Полная документация (англ.)

---

## 🎮 Пример использования

### 1. Создай тему

```python
# music/themes/cyberpunk.py

from .base import BaseTheme

class CyberpunkTheme(BaseTheme):
    name = 'cyberpunk'
    display_name = 'Cyberpunk 2077'
    description = 'Неоновый футуристичный дизайн'
    
    def get_static_css(self):
        return ['css/cyberpunk.css', 'css/neon-effects.css']
    
    def get_static_js(self):
        return ['js/glitch-effects.js']
```

### 2. Создай стили

```css
/* static/css/cyberpunk.css */

:root {
    --neon-cyan: #00fff9;
    --neon-pink: #ff006e;
    --neon-yellow: #ffbe0b;
}

.music-card {
    background: #0a0a0a;
    border: 2px solid var(--neon-cyan);
    box-shadow: 0 0 20px var(--neon-cyan);
    transition: all 0.3s;
}

.music-card:hover {
    border-color: var(--neon-pink);
    box-shadow: 0 0 40px var(--neon-pink);
    transform: translateY(-10px);
}
```

### 3. Зарегистрируй

```python
# music/apps.py

from music.themes.cyberpunk import CyberpunkTheme

def ready(self):
    from music.themes import registry
    registry.register(CyberpunkTheme)
    registry.set_active_theme('cyberpunk')
```

### ✅ Готово!

---

## 🎨 Встроенные темы

### 🎮 Steam Gaming Theme
```python
registry.set_active_theme('steam')
```
- Glass morphism эффекты
- Игровые карусели
- Featured баннеры
- Плавные анимации

### ✨ Minimal Clean Theme
```python
registry.set_active_theme('minimal')
```
- Минималистичный дизайн
- Быстрая загрузка
- Dark mode поддержка
- Нет JS-зависимостей

---

## 🔧 API Reference

### BaseTheme

```python
class BaseTheme:
    # Метаданные
    name: str                    # Уникальное имя
    display_name: str            # Отображаемое имя
    description: str             # Описание
    author: str                  # Автор
    version: str                 # Версия
    
    # Ассеты
    def get_static_css() -> list[str]
    def get_static_js() -> list[str]
    
    # Шаблоны
    def get_card_template() -> str
    def get_player_template() -> str
    def get_index_template() -> str
    def get_upload_template() -> str
    
    # Конфигурация
    def get_theme_config() -> dict
```

### ThemeRegistry

```python
from music.themes import registry

# Регистрация
registry.register(MyTheme)

# Получение
theme = registry.get_theme('mytheme')

# Активация
registry.set_active_theme('mytheme')

# Текущая
active = registry.get_active_theme()

# Список
themes = registry.list_themes()
```

---

## 💡 Use Cases

### 1. Быстрый MVP
Используй Steam тему как есть - красиво и сразу.

### 2. Под бренд клиента
Создай тему с цветами бренда за 5 минут.

### 3. A/B тестирование
Переключай темы для разных групп пользователей.

### 4. White-label продукт
Один код - множество визуальных вариантов.

---

## 📈 Roadmap

- [x] Базовая архитектура
- [x] Steam тема
- [x] Minimal тема
- [ ] UI для переключения тем
- [ ] Theme marketplace
- [ ] Live preview
- [ ] Export/import
- [ ] Наследование тем

---

## 👍 Best Practices

1. **Называй четко** - `name` должно быть lowercase
2. **Документируй** - Добавляй docstrings
3. **Минимальный CSS** - Только что нужно
4. **Reuse** - Наследуй BaseTheme
5. **Тестируй** - На разных экранах

---

## 🔗 Ссылки

- [Django Documentation](https://docs.djangoproject.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [FontAwesome Icons](https://fontawesome.com/)

---

Сделано с ❤️ для Music Stream
