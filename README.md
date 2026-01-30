# 🎵 Music Stream App

**Premium music streaming application** с четырьмя UI дизайн-системами: Apple Glass Effects, Steam Gaming Cards, Spotify Minimalism, и MSI Gaming Vibes.

![Version](https://img.shields.io/badge/version-2.0.0-red.svg)
![Django](https://img.shields.io/badge/django-5.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![UI Components](https://img.shields.io/badge/UI_components-108KB-orange.svg)

---

## ✨ Features

### 🎵 Core Functionality
- ✅ Music upload (MP3, FLAC, WAV, M4A, OGG)
- ✅ High-quality audio streaming
- ✅ Cover image support
- ✅ Metadata management (title, artist, album, year, genre)
- ✅ Search & filtering
- ✅ Download tracks
- ✅ Responsive player interface
- ✅ Progressive Web App (PWA)

### 🎨 Design Systems

#### 1. **Apple Glass Effects** (37.1 KB)
- Liquid glass morphism with backdrop-filter blur
- Dynamic glass layers (layer-1, layer-2, layer-3)
- Context-aware blur adjustments
- Scroll-reactive elevations
- Hover depth effects
- Floating particle animations
- Specular highlights & edge lighting

#### 2. **Steam Gaming Cards** (35.2 KB)
- Grid cards with 3:4 aspect ratio
- Interactive carousels with drag-to-scroll
- Featured hero banners (21:9 format)
- Quick action buttons (like, playlist, download)
- Play overlays with 80px circular buttons
- Category pills with horizontal scrolling
- Progress tracking & keyboard navigation

#### 3. **Spotify Minimalism** (23.0 KB)
- Sticky navigation with scroll reveal
- Browser history integration (back/forward)
- Breadcrumb navigation
- Compact sidebar with hover expand (72px → 280px)
- Minimal cards with green play button (#1db954)
- Pill filters & icon buttons
- Smooth page transitions
- Ctrl+K search shortcut

#### 4. **MSI Gaming Vibes** (13.0 KB)
- RGB glow animations
- Angular clip-path designs
- Performance stats widgets
- Neon red accents with pulse effects
- Hexagon background patterns
- Dragon-themed accents
- Scanline CRT effects
- Gaming-style buttons & inputs

---

## 📊 Stats

| Component | Files | Size | Minified |
|-----------|-------|------|----------|
| Glass Effects | 3 files | 37.1 KB | ~12 KB |
| Steam Gaming | 4 files | 35.2 KB | ~11 KB |
| Spotify Minimal | 4 files | 23.0 KB | ~7.5 KB |
| MSI Gaming | 1 file | 13.0 KB | ~4.2 KB |
| **Total** | **12 files** | **108.3 KB** | **~35 KB** |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Django 5.1+
- Modern browser with backdrop-filter support

### Installation

```bash
# Clone repository
git clone https://github.com/vitorpixel-6436/music-stream-app.git
cd music-stream-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Access
- **App**: http://localhost:8000/
- **Admin**: http://localhost:8000/admin/
- **Upload**: http://localhost:8000/upload/

---

## 📚 UI Components Guide

Подробная документация по всем компонентам: **[COMPONENTS.md](COMPONENTS.md)**

### Quick Examples

#### Glass Card
```html
<div class="glass-layer-2 glass-radius-xl glass-edge-light p-6" data-glass-hover="depth">
  <h3>Glass Card</h3>
  <p>With dynamic effects</p>
</div>
```

#### Steam Card
```html
<div class="steam-card" data-track-id="123">
  <div class="steam-card-cover">
    <img src="cover.jpg" class="steam-card-image">
  </div>
  <div class="steam-card-info">
    <h3 class="steam-card-title">Track Name</h3>
    <p class="steam-card-artist">Artist</p>
  </div>
</div>
```

#### Spotify Card
```html
<div class="spotify-card" data-track-id="123">
  <div class="spotify-card-image">
    <img src="cover.jpg">
    <div class="spotify-card-play">
      <i class="fas fa-play"></i>
    </div>
  </div>
  <h3 class="spotify-card-title">Track</h3>
</div>
```

#### MSI Button
```html
<button class="msi-btn rgb-glow">
  <i class="fas fa-play"></i>
  Play Now
</button>
```

---

## 🎯 Project Structure

```
music-stream-app/
├── music/
│   ├── static/
│   │   ├── css/
│   │   │   ├── glass-liquid.css        # Apple glass base (13.0 KB)
│   │   │   ├── glass-dynamics.css      # Dynamic effects (10.7 KB)
│   │   │   ├── steam-cards.css         # Gaming cards (12.9 KB)
│   │   │   ├── steam-carousel.css      # Carousels (9.9 KB)
│   │   │   ├── spotify-minimal.css     # Minimalism (10.6 KB)
│   │   │   └── msi-gaming.css          # Gaming vibes (13.0 KB)
│   │   │
│   │   └── js/
│   │       ├── glass-dynamics.js       # Glass system (13.4 KB)
│   │       ├── steam-carousel.js       # Carousel logic (12.4 KB)
│   │       └── spotify-minimal.js      # Spotify UI (12.4 KB)
│   │
│   ├── templates/music/
│   │   ├── base.html               # Base template with all systems
│   │   ├── index.html              # Home with Steam + Glass
│   │   └── upload.html             # Upload with Spotify minimal
│   │
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── COMPONENTS.md              # Full UI documentation (16.9 KB)
├── README.md                  # This file
├── requirements.txt
└── manage.py
```

---

## 💻 Tech Stack

### Backend
- **Django 5.1** - Web framework
- **Pillow** - Image processing
- **Python 3.10+** - Programming language

### Frontend
- **Tailwind CSS** - Utility-first CSS framework
- **Font Awesome 6.5** - Icon library
- **Inter & Orbitron** - Google Fonts
- **Vanilla JavaScript** - No dependencies

### UI Systems
- **Glass Morphism** - backdrop-filter, blur effects
- **Clip-path** - Angular gaming designs
- **CSS Grid** - Responsive layouts
- **CSS Animations** - RGB glows, neon pulses
- **Intersection Observer** - Fade-in animations
- **History API** - Browser navigation

---

## ⚙️ Configuration

### CSS Load Order (Important!)

```html
<!-- 1. Base glass effects -->
<link rel="stylesheet" href="css/glass-liquid.css">
<link rel="stylesheet" href="css/glass-dynamics.css">

<!-- 2. Component libraries -->
<link rel="stylesheet" href="css/steam-cards.css">
<link rel="stylesheet" href="css/steam-carousel.css">
<link rel="stylesheet" href="css/spotify-minimal.css">
<link rel="stylesheet" href="css/msi-gaming.css">

<!-- 3. Custom overrides -->
<link rel="stylesheet" href="css/custom.css">
```

### JavaScript Load Order

```html
<!-- 1. Glass dynamics (first) -->
<script src="js/glass-dynamics.js" defer></script>

<!-- 2. Component controllers -->
<script src="js/steam-carousel.js" defer></script>
<script src="js/spotify-minimal.js" defer></script>

<!-- 3. Page-specific scripts -->
<script src="js/page.js" defer></script>
```

---

## 🎮 Features Showcase

### 1. Glass Effects
- **Layers**: 3 уровня глубины (layer-1/2/3)
- **Tints**: Red, blue, purple colored glass
- **Radius**: 5 размеров (sm → 2xl)
- **Interactive**: Pressable, hover-lift
- **Dynamic**: Scroll-reactive, context-aware
- **Particles**: Floating background animation

### 2. Steam Gaming
- **Cards**: 3:4 aspect, hover lift, quick actions
- **Carousel**: Drag scroll, keyboard nav, progress bar
- **Featured**: 21:9 hero banner, gradient overlays
- **Pills**: Category filters, horizontal scroll
- **Grid**: Responsive auto-fill layout

### 3. Spotify Minimal
- **Navigation**: Sticky reveal, blur on scroll
- **Breadcrumbs**: Home › Current Page
- **Search**: Ctrl+K shortcut, auto-clear
- **Sidebar**: Compact mode (72px → 280px)
- **Cards**: Green play button, minimal design
- **Transitions**: Smooth page navigation

### 4. MSI Gaming
- **RGB Glow**: Animated box-shadow effects
- **Angular**: Clip-path polygon designs
- **Neon**: Pulsing text shadows
- **Hexagons**: Background pattern overlay
- **Stats**: Performance widget cards
- **Scanlines**: CRT monitor effect

---

## 📱 Responsive Design

| Breakpoint | Width | Layout Changes |
|------------|-------|----------------|
| **Mobile** | <640px | 2-col grid, hidden breadcrumbs, full-width search |
| **Tablet** | 640-1023px | 3-col grid, compact navigation |
| **Laptop** | 1024-1919px | 4-col grid, full features |
| **Desktop** | ≥1920px | 5-col grid, max 1920px container |

---

## ♿ Accessibility

- ✅ ARIA labels on interactive elements
- ✅ Keyboard navigation support
- ✅ Focus-visible styles (2px outline)
- ✅ Semantic HTML
- ✅ Alt text on images
- ✅ `prefers-reduced-motion` support
- ✅ Color contrast ratios (WCAG AA)

---

## 🚀 Performance

### Optimizations
- **CSS**: 108 KB → 35 KB (minified + gzip)
- **JavaScript**: Defer loading, no blocking
- **Images**: Lazy loading support
- **Fonts**: Preconnect to Google Fonts
- **CSS Containment**: `contain: layout style paint`
- **Intersection Observer**: Only animate visible elements

### Lighthouse Score Target
- Performance: 90+
- Accessibility: 95+
- Best Practices: 90+
- SEO: 100

---

## 🔧 Development

### Adding New Pages

1. Create template extending `base.html`:
```django
{% extends 'music/base.html' %}

{% block breadcrumbs %}
<span class="spotify-breadcrumb-separator">›</span>
<div class="spotify-breadcrumb-item active">Your Page</div>
{% endblock %}

{% block content %}
<!-- Your content -->
{% endblock %}
```

2. Choose UI style:
- Glass: `glass-layer-2 glass-radius-xl`
- Steam: `steam-card` or `steam-grid`
- Spotify: `spotify-card` or `spotify-row-item`
- MSI: `msi-card` or `msi-btn`

3. Add animations:
- Glass: `data-glass-hover="depth"`
- Spotify: `data-fade-in`
- MSI: `class="rgb-glow"`

---

## 📝 Release Notes

### Version 2.0.0 (2026-01-30)

#### ✨ New Features
- ✅ Complete UI system with 4 design languages
- ✅ 108 KB of premium CSS components
- ✅ 38 KB of JavaScript controllers
- ✅ Comprehensive documentation (COMPONENTS.md)
- ✅ MSI Gaming Vibes theme
- ✅ Spotify Minimalism components
- ✅ Steam Gaming Cards & Carousels
- ✅ Apple Glass Effects system

#### 🔧 Improvements
- Responsive design for all breakpoints
- Accessibility enhancements
- Performance optimizations
- Browser compatibility improvements

#### 📚 Documentation
- Full component showcase
- Integration examples
- Best practices guide
- Accessibility guidelines

---

## 🔗 Links

- **Repository**: https://github.com/vitorpixel-6436/music-stream-app
- **Components Guide**: [COMPONENTS.md](COMPONENTS.md)
- **Issues**: https://github.com/vitorpixel-6436/music-stream-app/issues
- **Releases**: https://github.com/vitorpixel-6436/music-stream-app/releases

---

## 👥 Author

**vitorpixel-6436**  
Email: vitorleitye6436@gmail.com

---

## 📜 License

MIT License - see LICENSE file for details

---

## 🚀 Roadmap

### v2.1.0 (Planned)
- [ ] Плейлисты и коллекции
- [ ] Социальные функции
- [ ] Lyrics интеграция
- [ ] Тёмная/светлая тема переключатель
- [ ] Продвинутый аудиоплеер с эквалайзером

### v2.2.0 (Future)
- [ ] Real-time collaboration
- [ ] Live streaming support
- [ ] Mobile apps (iOS/Android)
- [ ] Desktop apps (Electron)

---

## 🔥 Support

Понравился проект? Поставь ⭐ на GitHub!

---

**Made with ❤️ using Django, Tailwind CSS & Vanilla JavaScript**  
**© 2026 Music Stream App. All rights reserved.**
