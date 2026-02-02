# Steam UI Framework - Installation Guide

## 📦 Installation Methods

### Method 1: Install from GitHub Release (Recommended - No Git Required)

**For users without Git installed:**

1. Download the latest release wheel file from [Releases](https://github.com/vitorpixel-6436/music-stream-app/releases)
2. Install directly:

```bash
pip install steam_ui_framework-1.1.0-py3-none-any.whl
```

Or install from URL:

```bash
pip install https://github.com/vitorpixel-6436/music-stream-app/releases/download/v1.1.0/steam_ui_framework-1.1.0-py3-none-any.whl
```

### Method 2: Install from ZIP (No Git Required)

```bash
# Download ZIP archive
pip install https://github.com/vitorpixel-6436/music-stream-app/archive/refs/heads/main.zip
```

### Method 3: Install with Git

**If you have Git installed:**

```bash
pip install git+https://github.com/vitorpixel-6436/music-stream-app.git
```

### Method 4: Install from PyPI (Coming Soon)

```bash
pip install steam-ui-framework
```

---

## 🔧 Building from Source

### Prerequisites

- Python 3.8+
- pip 21.0+

### Steps

1. **Clone the repository:**

```bash
git clone https://github.com/vitorpixel-6436/music-stream-app.git
cd music-stream-app
```

2. **Install build tools:**

```bash
pip install build wheel
```

3. **Build the package:**

```bash
python -m build
```

This creates:
- `dist/steam_ui_framework-1.1.0-py3-none-any.whl`
- `dist/steam-ui-framework-1.1.0.tar.gz`

4. **Install the built package:**

```bash
pip install dist/steam_ui_framework-1.1.0-py3-none-any.whl
```

---

## 🐛 Troubleshooting

### Error: "Cannot find command 'git'"

**Problem:** Git is not installed or not in PATH.

**Solutions:**

1. **Option A: Install Git**
   - Windows: Download from [git-scm.com](https://git-scm.com/download/win)
   - Linux: `sudo apt-get install git`
   - macOS: `brew install git`

2. **Option B: Use Method 1 or 2** (No Git required)

### Error: "No matching distribution found"

**Solution:** Update pip:

```bash
python -m pip install --upgrade pip
```

### Error: "Could not find a version that satisfies the requirement"

**Solution:** Check Python version (requires 3.8+):

```bash
python --version
```

### Static files not loading in Django

**Solution:** Run collectstatic:

```bash
python manage.py collectstatic
```

And add to `INSTALLED_APPS` in settings.py:

```python
INSTALLED_APPS = [
    # ...
    'steam_ui',
]
```

---

## ✅ Verify Installation

Test the installation:

```python
import steam_ui
print(steam_ui.__version__)  # Should print: 1.1.0

from steam_ui import Card, Carousel, PlayerBar
print("Steam UI Framework installed successfully!")
```

---

## 📚 Next Steps

- Read [README.md](README.md) for usage examples
- Check [Documentation](https://github.com/vitorpixel-6436/music-stream-app/wiki)
- Join discussions on [GitHub Discussions](https://github.com/vitorpixel-6436/music-stream-app/discussions)

---

## 📞 Support

If you encounter issues:

1. Check [Issues](https://github.com/vitorpixel-6436/music-stream-app/issues)
2. Search [Stack Overflow](https://stackoverflow.com/questions/tagged/steam-ui-framework)
3. Create a new issue with:
   - Python version (`python --version`)
   - pip version (`pip --version`)
   - OS and version
   - Full error traceback

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.
