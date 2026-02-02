# 🚀 Quick Start - Steam UI Framework (No Git Required)

## ❌ Problem: "Cannot find command 'git'"

If you see this error:

```
ERROR: Cannot find command 'git' - do you have 'git' installed and in your PATH?
```

**Don't worry!** You can install Steam UI Framework **without Git**.

---

## ✅ Solution: Install from ZIP (One Command)

### Step 1: Open Terminal/PowerShell

Windows:
- Press `Win + X`
- Select "Windows PowerShell" or "Terminal"

Linux/Mac:
- Open Terminal

### Step 2: Activate Your Virtual Environment

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Steam UI Framework

**Copy and paste this ONE command:**

```bash
pip install https://github.com/vitorpixel-6436/music-stream-app/archive/refs/heads/main.zip
```

**That's it!** ✨

---

## ✅ Verify Installation

Test that it worked:

```python
python
>>> import steam_ui
>>> print(steam_ui.__version__)
1.1.0
>>> exit()
```

If you see `1.1.0`, installation was successful! 🎉

---

## 🛠️ Django Setup

### 1. Add to `settings.py`:

```python
INSTALLED_APPS = [
    # ... other apps
    'steam_ui',  # Add this line
]
```

### 2. Use in templates:

```django
{% load steam_ui %}

{% steam_css %}

{% steam_card track %}
{% steam_carousel tracks title="Recent" %}
{% steam_player_bar current_track %}

{% steam_js %}
```

### 3. Collect static files:

```bash
python manage.py collectstatic
```

**Done!** ✅

---

## 🐛 Still Having Issues?

### Error: "No matching distribution found"

**Solution:** Update pip first:

```bash
python -m pip install --upgrade pip
```

Then try installation again.

### Error: "Permission denied"

**Solution:** Use `--user` flag:

```bash
pip install --user https://github.com/vitorpixel-6436/music-stream-app/archive/refs/heads/main.zip
```

### Requirements.txt Conflict

If your `requirements.txt` has this line:

```txt
git+https://github.com/vitorpixel-6436/music-stream-app.git
```

**Replace it with:**

```txt
steam-ui-framework @ https://github.com/vitorpixel-6436/music-stream-app/archive/refs/heads/main.zip
```

Or just install manually using the command above.

---

## 📚 Need More Help?

- 📖 [Full Installation Guide](INSTALL.md)
- 📝 [Complete Documentation](README.md)
- 🐛 [Report Issues](https://github.com/vitorpixel-6436/music-stream-app/issues)

---

## ✨ Alternative: Download as Wheel

If ZIP method doesn't work:

1. Go to [Releases](https://github.com/vitorpixel-6436/music-stream-app/releases)
2. Download `steam_ui_framework-1.1.0-py3-none-any.whl`
3. Install:

```bash
pip install steam_ui_framework-1.1.0-py3-none-any.whl
```

---

**Quick Summary:**

```bash
# One command installation (no Git needed):
pip install https://github.com/vitorpixel-6436/music-stream-app/archive/refs/heads/main.zip

# Add to settings.py:
INSTALLED_APPS = ['steam_ui']

# Collect static files:
python manage.py collectstatic

# Start using:
{% load steam_ui %}
{% steam_card track %}
```

**That's all you need!** 🚀
