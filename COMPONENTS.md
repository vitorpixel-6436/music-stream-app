# 🎨 Music Stream UI Components Library

Полное руководство по всем UI компонентам проекта Music Stream App.  
Последнее обновление: **30 января 2026**

---

## 📚 Оглавление

1. [Glass Effects (Apple-style)](#glass-effects)
2. [Steam Gaming Cards](#steam-gaming-cards)
3. [Spotify Minimalism](#spotify-minimalism)
4. [Примеры интеграции](#integration-examples)
5. [Best Practices](#best-practices)

---

## 1. Glass Effects (Apple-style)

### 1.1 Liquid Glass

**Файл**: `music/static/css/glass-liquid.css`  
**Размер**: 13.0 KB

#### Основные классы:

```html
<!-- Base glass layer -->
<div class="glass-layer-1">Content</div>
<div class="glass-layer-2">Content</div>
<div class="glass-layer-3">Content</div>

<!-- Glass with colored tints -->
<div class="glass-red-tint">Red tinted glass</div>
<div class="glass-blue-tint">Blue tinted glass</div>
<div class="glass-purple-tint">Purple tinted glass</div>

<!-- Border radius utilities -->
<div class="glass-radius-sm">8px radius</div>
<div class="glass-radius-md">12px radius</div>
<div class="glass-radius-lg">16px radius</div>
<div class="glass-radius-xl">24px radius</div>
<div class="glass-radius-2xl">32px radius</div>

<!-- Interactive states -->
<button class="glass-pressable">Pressable button</button>
<div class="glass-hover-lift">Lifts on hover</div>
```

#### Specular highlights:

```html
<div class="glass-layer-2 glass-specular-top">
  <!-- White gradient at top -->
</div>

<div class="glass-layer-2 glass-specular-bottom">
  <!-- White gradient at bottom -->
</div>
```

#### Edge lighting:

```html
<div class="glass-edge-light">
  <!-- Subtle edge glow -->
</div>

<div class="glass-edge-red">
  <!-- Red edge glow -->
</div>
```

---

### 1.2 Dynamic Glass

**Файл**: `music/static/css/glass-dynamics.css` + `music/static/js/glass-dynamics.js`  
**Размер**: 10.7 KB (CSS) + 13.4 KB (JS)

#### Context-aware glass:

```html
<!-- Parent wrapper -->
<div data-glass-context>
  <!-- Children automatically get blur adjustments -->
  <div class="glass-layer-2">Card 1</div>
  <div class="glass-layer-2">Card 2</div>
</div>
```

#### Scroll-reactive effects:

```html
<!-- Elevates on scroll -->
<div data-glass-scroll="elevate">Navbar</div>

<!-- Fades on scroll -->
<div data-glass-scroll="fade">Header</div>

<!-- Reveals on scroll -->
<div data-glass-scroll="reveal">Content</div>
```

#### Hover depth:

```html
<div data-glass-hover="depth">Card with depth on hover</div>
<div data-glass-hover="glow">Card with glow on hover</div>
```

#### Particle effects:

```html
<!-- On body tag -->
<body data-glass-particles>
  <!-- Floating particles in background -->
</body>
```

---

## 2. Steam Gaming Cards

### 2.1 Steam Cards Grid

**Файл**: `music/static/css/steam-cards.css`  
**Размер**: 12.9 KB

#### Basic card:

```html
<div class="steam-card" data-track-id="123">
  <!-- Cover image -->
  <div class="steam-card-cover">
    <img src="cover.jpg" class="steam-card-image" alt="Track">
  </div>
  
  <!-- Overlay gradient -->
  <div class="steam-card-overlay"></div>
  
  <!-- Quick actions -->
  <div class="steam-card-actions">
    <button class="steam-action-btn" data-action="like">
      <i class="far fa-heart"></i>
    </button>
    <button class="steam-action-btn" data-action="add-playlist">
      <i class="fas fa-plus"></i>
    </button>
    <button class="steam-action-btn" data-action="download">
      <i class="fas fa-download"></i>
    </button>
  </div>
  
  <!-- Play overlay -->
  <div class="steam-play-overlay">
    <button class="steam-play-btn">
      <i class="fas fa-play"></i>
    </button>
  </div>
  
  <!-- Track info -->
  <div class="steam-card-info">
    <h3 class="steam-card-title">Track Name</h3>
    <p class="steam-card-artist">Artist Name</p>
    <div class="steam-card-meta">
      <span><i class="far fa-clock"></i> 3:45</span>
      <span class="steam-card-badge">New</span>
    </div>
  </div>
</div>
```

#### Grid layout:

```html
<div class="steam-grid">
  <!-- Cards automatically arrange in responsive grid -->
  <div class="steam-card">...</div>
  <div class="steam-card">...</div>
  <div class="steam-card">...</div>
</div>
```

**Breakpoints:**
- Desktop (≥1920px): 340px cards
- Laptop (1024-1919px): 320px cards
- Tablet (640-1023px): 300px cards
- Mobile (<640px): 2 columns, 160px cards

---

### 2.2 Steam Carousel

**Файл**: `music/static/css/steam-carousel.css` + `music/static/js/steam-carousel.js`  
**Размер**: 9.9 KB (CSS) + 12.4 KB (JS)

#### Full carousel:

```html
<section class="steam-carousel-section" data-glass-context>
  <!-- Header with navigation -->
  <div class="steam-carousel-header">
    <h2 class="steam-carousel-title">
      <i class="fas fa-fire"></i>
      Recently Added
    </h2>
    <div class="steam-carousel-nav">
      <button class="steam-carousel-arrow" data-carousel-prev>
        <i class="fas fa-chevron-left"></i>
      </button>
      <button class="steam-carousel-arrow" data-carousel-next>
        <i class="fas fa-chevron-right"></i>
      </button>
    </div>
  </div>
  
  <!-- Carousel wrapper -->
  <div class="steam-carousel-wrapper">
    <div class="steam-carousel">
      <!-- Items -->
      <div class="steam-carousel-item">
        <div class="steam-carousel-card" data-track-id="1">
          <img src="cover.jpg" class="steam-carousel-card-image">
          <div class="steam-carousel-card-overlay">
            <h3 class="steam-carousel-card-title">Track Name</h3>
            <p class="steam-carousel-card-artist">Artist</p>
          </div>
          <div class="steam-carousel-card-play">
            <i class="fas fa-play"></i>
          </div>
        </div>
      </div>
      <!-- More items... -->
    </div>
    
    <!-- Progress bar -->
    <div class="steam-carousel-progress">
      <div class="steam-carousel-progress-bar"></div>
    </div>
  </div>
</section>
```

**JavaScript функции:**
- Drag to scroll (mouse & touch)
- Keyboard navigation (← → Home End)
- Auto-disable arrows at edges
- Smooth snap scrolling
- Progress bar tracking

---

### 2.3 Featured Banner

```html
<div class="steam-featured" data-track-id="123" data-album-id="1">
  <!-- Background -->
  <div class="steam-featured-bg">
    <img src="cover.jpg" class="steam-featured-image">
  </div>
  
  <!-- Gradient overlay -->
  <div class="steam-featured-overlay"></div>
  
  <!-- Content -->
  <div class="steam-featured-content">
    <div class="steam-featured-label">
      <i class="fas fa-star"></i>
      FEATURED TRACK
    </div>
    <h1 class="steam-featured-title">Track Title</h1>
    <p class="steam-featured-artist">Artist Name</p>
    <p class="steam-featured-description">Description text...</p>
    
    <div class="steam-featured-actions">
      <button class="steam-featured-btn steam-featured-btn-primary">
        <i class="fas fa-play"></i> Play Now
      </button>
      <button class="steam-featured-btn steam-featured-btn-secondary">
        <i class="fas fa-download"></i> Download
      </button>
    </div>
  </div>
</div>
```

---

### 2.4 Category Pills

```html
<div class="steam-category-pills">
  <button class="steam-category-pill active" data-category="all">
    <i class="fas fa-fire mr-2"></i>All Tracks
  </button>
  <button class="steam-category-pill" data-category="recent">
    <i class="fas fa-clock mr-2"></i>Recent
  </button>
  <button class="steam-category-pill" data-category="popular">
    <i class="fas fa-chart-line mr-2"></i>Popular
  </button>
</div>
```

---

## 3. Spotify Minimalism

### 3.1 Sticky Navigation

**Файл**: `music/static/css/spotify-minimal.css` + `music/static/js/spotify-minimal.js`  
**Размер**: 10.6 KB (CSS) + 12.4 KB (JS)

```html
<nav class="spotify-nav">
  <div class="spotify-nav-content">
    <!-- Back/Forward arrows -->
    <div class="spotify-nav-arrows">
      <button class="spotify-nav-arrow" data-nav="back">
        <i class="fas fa-chevron-left"></i>
      </button>
      <button class="spotify-nav-arrow" data-nav="forward">
        <i class="fas fa-chevron-right"></i>
      </button>
    </div>
    
    <!-- Breadcrumbs -->
    <div class="spotify-breadcrumbs">
      <div class="spotify-breadcrumb-item">
        <a href="/"><i class="fas fa-home"></i></a>
      </div>
      <span class="spotify-breadcrumb-separator">›</span>
      <div class="spotify-breadcrumb-item active">
        Current Page
      </div>
    </div>
    
    <!-- Search -->
    <div class="spotify-search">
      <i class="fas fa-search spotify-search-icon"></i>
      <input type="text" 
             class="spotify-search-input" 
             placeholder="What do you want to listen to?">
    </div>
  </div>
</nav>
```

**JavaScript поведение:**
- Становится непрозрачным при scroll > 50px
- Back/forward кнопки управляют browser history
- Ctrl+K / Cmd+K фокусирует search

---

### 3.2 Minimal Cards

```html
<div class="spotify-card" data-track-id="123">
  <!-- Image with play button -->
  <div class="spotify-card-image">
    <img src="cover.jpg" alt="Track">
    <div class="spotify-card-play">
      <i class="fas fa-play"></i>
    </div>
  </div>
  
  <!-- Info -->
  <h3 class="spotify-card-title">Track Name</h3>
  <p class="spotify-card-subtitle">Artist • Album</p>
</div>
```

**Hover эффекты:**
- translateY(-2px)
- Play button: opacity 0 → 1
- Image: scale(1.05)
- Green play button (#1db954)

---

### 3.3 Row Items

```html
<div class="spotify-row-item" data-track-id="123">
  <!-- Image -->
  <div class="spotify-row-item-image">
    <img src="thumb.jpg" alt="Track">
  </div>
  
  <!-- Info -->
  <div class="spotify-row-item-info">
    <h4 class="spotify-row-item-title">Track Name</h4>
    <p class="spotify-row-item-subtitle">Artist Name</p>
  </div>
  
  <!-- Actions (show on hover) -->
  <div class="spotify-row-item-actions">
    <button class="spotify-icon-btn">
      <i class="far fa-heart"></i>
    </button>
    <button class="spotify-icon-btn">
      <i class="fas fa-ellipsis-h"></i>
    </button>
  </div>
</div>
```

---

### 3.4 Pill Buttons

```html
<!-- Filter pills -->
<div class="flex gap-2">
  <button class="spotify-pill active">All</button>
  <button class="spotify-pill">Rock</button>
  <button class="spotify-pill">Pop</button>
  <button class="spotify-pill">Jazz</button>
</div>
```

---

### 3.5 Compact Sidebar

```html
<aside id="sidebar" class="spotify-sidebar-compact">
  <!-- Expands from 72px to 280px on hover -->
  <nav>
    <a href="/">
      <i class="fas fa-home sidebar-icon"></i>
      <span class="sidebar-text">Home</span>
    </a>
  </nav>
</aside>
```

**CSS:**
```css
.spotify-sidebar-compact {
  width: 72px;
  transition: width 0.3s ease;
}

.spotify-sidebar-compact:hover {
  width: 280px;
}

.spotify-sidebar-compact .sidebar-text {
  opacity: 0;
  transition: opacity 0.2s;
}

.spotify-sidebar-compact:hover .sidebar-text {
  opacity: 1;
  transition-delay: 0.1s;
}
```

---

### 3.6 Section Headers

```html
<div class="spotify-section-header">
  <div>
    <h2 class="spotify-section-title">Section Title</h2>
    <p class="spotify-section-subtitle">Optional subtitle</p>
  </div>
  <a href="#" class="spotify-section-link">Show All</a>
</div>
```

---

## 4. Примеры интеграции

### 4.1 Hero Section (Glass + Steam + Spotify)

```html
<!-- Spotify header -->
<div class="spotify-section-header mb-12" data-fade-in>
  <div>
    <h1 class="spotify-section-title text-5xl">Your Library</h1>
    <p class="spotify-section-subtitle">Discover amazing music</p>
  </div>
</div>

<!-- Steam featured banner with glass effects -->
<div class="steam-featured" data-glass-context data-glass-hover="depth">
  <!-- Banner content -->
</div>
```

---

### 4.2 Music Grid Page

```html
<!-- Spotify pills for filters -->
<div class="steam-category-pills mb-8">
  <button class="steam-category-pill active">All</button>
  <button class="steam-category-pill">Recent</button>
  <button class="steam-category-pill">Popular</button>
</div>

<!-- Steam carousel -->
<section class="steam-carousel-section mb-16">
  <!-- Carousel -->
</section>

<!-- Steam grid -->
<div class="steam-grid">
  <div class="steam-card" data-glass-hover="glow">...</div>
  <div class="steam-card" data-glass-hover="glow">...</div>
</div>
```

---

### 4.3 Upload Form

```html
<!-- Spotify minimal card -->
<div class="spotify-card p-8" data-fade-in>
  <h3 class="text-lg font-semibold mb-4">Track Information</h3>
  
  <div class="space-y-4">
    <input type="text" 
           class="w-full bg-white/5 px-4 py-3 rounded-lg border border-white/10 focus:border-white/30 outline-none"
           placeholder="Track Title">
  </div>
</div>
```

---

## 5. Best Practices

### 5.1 Порядок загрузки CSS

```html
<!-- 1. Base glass effects -->
<link rel="stylesheet" href="css/glass-liquid.css">
<link rel="stylesheet" href="css/glass-dynamics.css">

<!-- 2. Component libraries -->
<link rel="stylesheet" href="css/steam-cards.css">
<link rel="stylesheet" href="css/steam-carousel.css">
<link rel="stylesheet" href="css/spotify-minimal.css">

<!-- 3. Custom overrides -->
<link rel="stylesheet" href="css/custom.css">
```

---

### 5.2 Порядок загрузки JS

```html
<!-- 1. Glass dynamics (first, as it affects everything) -->
<script src="js/glass-dynamics.js" defer></script>

<!-- 2. Component controllers -->
<script src="js/steam-carousel.js" defer></script>
<script src="js/spotify-minimal.js" defer></script>

<!-- 3. Page-specific scripts -->
<script src="js/page.js" defer></script>
```

---

### 5.3 Комбинирование стилей

✅ **Правильно:**
```html
<div class="steam-card glass-layer-2" data-glass-hover="depth">
  <!-- Combines Steam card with glass effects -->
</div>
```

❌ **Неправильно:**
```html
<div class="glass-layer-1 glass-layer-2">
  <!-- Don't use multiple glass layers -->
</div>
```

---

### 5.4 Performance Tips

1. **Используйте `data-glass-context` для групп:**
   ```html
   <div data-glass-context>
     <div class="glass-layer-2">Card 1</div>
     <div class="glass-layer-2">Card 2</div>
   </div>
   ```

2. **Lazy load carousels:**
   ```javascript
   // Initialize only visible carousels
   const observer = new IntersectionObserver(entries => {
     entries.forEach(entry => {
       if (entry.isIntersecting) {
         new SteamCarousel(entry.target);
       }
     });
   });
   ```

3. **Используйте CSS containment:**
   ```css
   .steam-card {
     contain: layout style paint;
   }
   ```

---

### 5.5 Accessibility

```html
<!-- Always include aria labels -->
<button class="steam-carousel-arrow" 
        data-carousel-prev 
        aria-label="Previous items">
  <i class="fas fa-chevron-left" aria-hidden="true"></i>
</button>

<!-- Keyboard navigation support -->
<div class="steam-card" 
     tabindex="0" 
     role="button"
     data-track-id="123">
  <!-- Card content -->
</div>

<!-- Focus visible styles -->
<style>
.steam-card:focus-visible {
  outline: 2px solid white;
  outline-offset: 2px;
}
</style>
```

---

### 5.6 Responsive Design

```html
<!-- Mobile-first approach -->
<div class="
  p-4 lg:p-8
  text-sm lg:text-base
  grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4
">
  <!-- Content adapts to screen size -->
</div>
```

---

## 📦 Размеры файлов

| Файл | Размер | Минифицированный |
|------|--------|------------------|
| glass-liquid.css | 13.0 KB | ~4.2 KB |
| glass-dynamics.css | 10.7 KB | ~3.5 KB |
| glass-dynamics.js | 13.4 KB | ~4.8 KB |
| steam-cards.css | 12.9 KB | ~4.1 KB |
| steam-carousel.css | 9.9 KB | ~3.2 KB |
| steam-carousel.js | 12.4 KB | ~4.5 KB |
| spotify-minimal.css | 10.6 KB | ~3.4 KB |
| spotify-minimal.js | 12.4 KB | ~4.5 KB |
| **Всего** | **95.3 KB** | **~32 KB** |

---

## 🚀 Quick Start

### Минимальная интеграция:

```html
<!DOCTYPE html>
<html>
<head>
  <!-- Core styles -->
  <link rel="stylesheet" href="css/glass-liquid.css">
  <link rel="stylesheet" href="css/spotify-minimal.css">
</head>
<body>
  
  <!-- Spotify navigation -->
  <nav class="spotify-nav">
    <!-- Nav content -->
  </nav>
  
  <!-- Content -->
  <main>
    <div class="spotify-card">
      Hello World!
    </div>
  </main>
  
  <!-- Scripts -->
  <script src="js/spotify-minimal.js" defer></script>
</body>
</html>
```

---

## 📞 Support

Для вопросов и багрепортов:
- GitHub Issues: [music-stream-app/issues](https://github.com/vitorpixel-6436/music-stream-app/issues)
- Email: vitorleitye6436@gmail.com

---

**Создано с ❤️ для Music Stream App**  
**Версия**: 1.0.0  
**Дата**: 30 января 2026
