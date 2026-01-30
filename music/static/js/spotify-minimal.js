/**
 * SPOTIFY MINIMALISM
 * Stage 3.1: Clean, minimal UI interactions
 * 
 * Features:
 * - Sticky navigation with scroll detection
 * - Browser history integration
 * - Smooth page transitions
 * - Compact mode toggle
 */

// ============================================
// STICKY NAVIGATION
// ============================================
class SpotifyNavigation {
  constructor() {
    this.nav = document.querySelector('.spotify-nav');
    this.lastScroll = 0;
    this.threshold = 50;
    
    if (!this.nav) return;
    
    this.init();
  }
  
  init() {
    window.addEventListener('scroll', () => this.handleScroll(), { passive: true });
    this.handleScroll(); // Initial check
  }
  
  handleScroll() {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > this.threshold) {
      this.nav.classList.add('scrolled');
    } else {
      this.nav.classList.remove('scrolled');
    }
    
    this.lastScroll = currentScroll;
  }
}

// ============================================
// BROWSER HISTORY NAVIGATION
// ============================================
class BrowserNavigation {
  constructor() {
    this.backBtn = document.querySelector('[data-nav="back"]');
    this.forwardBtn = document.querySelector('[data-nav="forward"]');
    
    if (!this.backBtn || !this.forwardBtn) return;
    
    this.init();
  }
  
  init() {
    // Back button
    this.backBtn.addEventListener('click', () => {
      if (window.history.length > 1) {
        window.history.back();
      }
    });
    
    // Forward button
    this.forwardBtn.addEventListener('click', () => {
      window.history.forward();
    });
    
    // Update button states
    this.updateButtons();
    
    // Listen for navigation
    window.addEventListener('popstate', () => this.updateButtons());
  }
  
  updateButtons() {
    // Note: There's no direct way to check if forward is possible
    // This is a limitation of the History API
    
    // Disable back if at start
    if (window.history.length <= 1) {
      this.backBtn.disabled = true;
    } else {
      this.backBtn.disabled = false;
    }
  }
}

// ============================================
// COMPACT SIDEBAR TOGGLE
// ============================================
class CompactSidebarToggle {
  constructor() {
    this.sidebar = document.querySelector('#sidebar');
    this.toggleBtn = document.querySelector('[data-toggle="compact-sidebar"]');
    this.storageKey = 'spotify-sidebar-compact';
    
    if (!this.sidebar) return;
    
    this.init();
  }
  
  init() {
    // Restore state from localStorage
    const isCompact = localStorage.getItem(this.storageKey) === 'true';
    if (isCompact) {
      this.setCompact(true, false);
    }
    
    // Add toggle button if it doesn't exist
    if (!this.toggleBtn && this.sidebar) {
      this.createToggleButton();
    }
    
    // Listen for toggle
    if (this.toggleBtn) {
      this.toggleBtn.addEventListener('click', () => this.toggle());
    }
  }
  
  createToggleButton() {
    const btn = document.createElement('button');
    btn.className = 'spotify-icon-btn absolute top-4 right-4';
    btn.setAttribute('data-toggle', 'compact-sidebar');
    btn.setAttribute('title', 'Toggle compact mode');
    btn.innerHTML = '<i class="fas fa-bars"></i>';
    
    this.sidebar.appendChild(btn);
    this.toggleBtn = btn;
  }
  
  toggle() {
    const isCurrentlyCompact = this.sidebar.classList.contains('spotify-sidebar-compact');
    this.setCompact(!isCurrentlyCompact);
  }
  
  setCompact(compact, save = true) {
    if (compact) {
      this.sidebar.classList.add('spotify-sidebar-compact');
      if (this.toggleBtn) {
        this.toggleBtn.querySelector('i').className = 'fas fa-expand';
      }
    } else {
      this.sidebar.classList.remove('spotify-sidebar-compact');
      if (this.toggleBtn) {
        this.toggleBtn.querySelector('i').className = 'fas fa-bars';
      }
    }
    
    if (save) {
      localStorage.setItem(this.storageKey, compact);
    }
  }
}

// ============================================
// SMOOTH SEARCH
// ============================================
class SpotifySearch {
  constructor() {
    this.searchInput = document.querySelector('.spotify-search-input');
    this.searchForm = document.querySelector('.spotify-search')?.closest('form');
    
    if (!this.searchInput) return;
    
    this.init();
  }
  
  init() {
    // Clear button
    this.searchInput.addEventListener('input', (e) => {
      if (e.target.value) {
        this.showClearButton();
      } else {
        this.hideClearButton();
      }
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      // Ctrl/Cmd + K to focus search
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        this.searchInput.focus();
      }
      
      // Escape to blur
      if (e.key === 'Escape' && document.activeElement === this.searchInput) {
        this.searchInput.blur();
      }
    });
  }
  
  showClearButton() {
    if (this.searchInput.nextElementSibling?.classList.contains('clear-btn')) return;
    
    const clearBtn = document.createElement('button');
    clearBtn.type = 'button';
    clearBtn.className = 'clear-btn absolute right-4 top-1/2 -translate-y-1/2 text-white/60 hover:text-white transition-colors';
    clearBtn.innerHTML = '<i class="fas fa-times"></i>';
    clearBtn.addEventListener('click', () => {
      this.searchInput.value = '';
      this.searchInput.focus();
      this.hideClearButton();
    });
    
    this.searchInput.parentElement.style.position = 'relative';
    this.searchInput.parentElement.appendChild(clearBtn);
  }
  
  hideClearButton() {
    const clearBtn = this.searchInput.nextElementSibling;
    if (clearBtn?.classList.contains('clear-btn')) {
      clearBtn.remove();
    }
  }
}

// ============================================
// PAGE TRANSITIONS
// ============================================
class PageTransitions {
  constructor() {
    this.links = [];
    this.init();
  }
  
  init() {
    // Find all internal links
    this.links = document.querySelectorAll('a[href^="/"]:not([target="_blank"])');
    
    this.links.forEach(link => {
      link.addEventListener('click', (e) => this.handleClick(e));
    });
  }
  
  handleClick(e) {
    const link = e.currentTarget;
    const href = link.getAttribute('href');
    
    // Skip if special keys are pressed
    if (e.metaKey || e.ctrlKey || e.shiftKey) return;
    
    // Skip if same page
    if (href === window.location.pathname) {
      e.preventDefault();
      return;
    }
    
    // Add fade out animation
    e.preventDefault();
    document.body.style.opacity = '0.8';
    document.body.style.transition = 'opacity 0.2s ease';
    
    setTimeout(() => {
      window.location.href = href;
    }, 200);
  }
}

// ============================================
// CARD INTERACTIONS
// ============================================
class SpotifyCardController {
  constructor() {
    this.cards = [];
    this.init();
  }
  
  init() {
    this.cards = document.querySelectorAll('.spotify-card');
    
    this.cards.forEach(card => {
      // Play button
      const playBtn = card.querySelector('.spotify-card-play');
      if (playBtn) {
        playBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          this.playTrack(card);
        });
      }
      
      // Card click
      card.addEventListener('click', () => {
        this.openCard(card);
      });
    });
  }
  
  playTrack(card) {
    const trackId = card.dataset.trackId;
    console.log('🎵 Playing track:', trackId);
    
    // Emit event
    window.dispatchEvent(new CustomEvent('trackPlay', {
      detail: { trackId, card }
    }));
  }
  
  openCard(card) {
    const trackId = card.dataset.trackId;
    if (trackId) {
      window.location.href = `/player/${trackId}/`;
    }
  }
}

// ============================================
// ROW ITEM INTERACTIONS
// ============================================
class SpotifyRowController {
  constructor() {
    this.rows = [];
    this.init();
  }
  
  init() {
    this.rows = document.querySelectorAll('.spotify-row-item');
    
    this.rows.forEach(row => {
      row.addEventListener('click', (e) => {
        // Don't trigger if clicking on actions
        if (e.target.closest('.spotify-row-item-actions')) return;
        
        this.selectRow(row);
      });
      
      // Double click to play
      row.addEventListener('dblclick', () => {
        this.playRow(row);
      });
    });
  }
  
  selectRow(row) {
    // Remove selection from all
    this.rows.forEach(r => r.classList.remove('selected'));
    
    // Add to clicked
    row.classList.add('selected');
    
    const trackId = row.dataset.trackId;
    console.log('Selected track:', trackId);
  }
  
  playRow(row) {
    const trackId = row.dataset.trackId;
    console.log('🎵 Playing track:', trackId);
    
    window.dispatchEvent(new CustomEvent('trackPlay', {
      detail: { trackId, row }
    }));
  }
}

// ============================================
// PILL FILTERS
// ============================================
class SpotifyPillFilters {
  constructor() {
    this.pills = [];
    this.init();
  }
  
  init() {
    this.pills = document.querySelectorAll('.spotify-pill');
    
    this.pills.forEach(pill => {
      pill.addEventListener('click', () => {
        this.selectPill(pill);
      });
    });
  }
  
  selectPill(pill) {
    // Remove active from all
    this.pills.forEach(p => p.classList.remove('active'));
    
    // Add to clicked
    pill.classList.add('active');
    
    const filter = pill.dataset.filter;
    console.log('Filter changed:', filter);
    
    // Emit event
    window.dispatchEvent(new CustomEvent('filterChange', {
      detail: { filter }
    }));
  }
}

// ============================================
// FADE IN OBSERVER
// ============================================
class FadeInObserver {
  constructor() {
    this.elements = [];
    this.observer = null;
    this.init();
  }
  
  init() {
    this.elements = document.querySelectorAll('[data-fade-in]');
    
    if (this.elements.length === 0) return;
    
    this.observer = new IntersectionObserver(
      (entries) => this.handleIntersection(entries),
      {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      }
    );
    
    this.elements.forEach(el => this.observer.observe(el));
  }
  
  handleIntersection(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('spotify-fade-in');
        this.observer.unobserve(entry.target);
      }
    });
  }
}

// ============================================
// INITIALIZATION
// ============================================
class SpotifyUI {
  constructor() {
    this.navigation = null;
    this.browserNav = null;
    this.compactSidebar = null;
    this.search = null;
    this.pageTransitions = null;
    this.cardController = null;
    this.rowController = null;
    this.pillFilters = null;
    this.fadeInObserver = null;
    
    // Wait for DOM
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.init());
    } else {
      this.init();
    }
  }
  
  init() {
    // Initialize all systems
    this.navigation = new SpotifyNavigation();
    this.browserNav = new BrowserNavigation();
    this.compactSidebar = new CompactSidebarToggle();
    this.search = new SpotifySearch();
    this.pageTransitions = new PageTransitions();
    this.cardController = new SpotifyCardController();
    this.rowController = new SpotifyRowController();
    this.pillFilters = new SpotifyPillFilters();
    this.fadeInObserver = new FadeInObserver();
    
    console.log('✅ Spotify UI initialized');
  }
}

// ============================================
// AUTO-INITIALIZE
// ============================================
window.SpotifyUI = new SpotifyUI();

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    SpotifyUI,
    SpotifyNavigation,
    BrowserNavigation,
    CompactSidebarToggle,
    SpotifySearch,
    PageTransitions,
    SpotifyCardController,
    SpotifyRowController,
    SpotifyPillFilters,
    FadeInObserver,
  };
}
