/**
 * STEAM CAROUSEL CONTROLLER
 * Stage 2.1: Interactive carousel controls
 * 
 * Features:
 * - Arrow navigation
 * - Smooth scrolling
 * - Progress tracking
 * - Touch/swipe support
 * - Keyboard navigation
 * - Auto-hide navigation
 */

// ============================================
// CAROUSEL CLASS
// ============================================
class SteamCarousel {
  constructor(element) {
    this.wrapper = element;
    this.carousel = element.querySelector('.steam-carousel');
    this.prevBtn = element.querySelector('[data-carousel-prev]');
    this.nextBtn = element.querySelector('[data-carousel-next]');
    this.progressBar = element.querySelector('.steam-carousel-progress-bar');
    
    if (!this.carousel) return;
    
    this.scrollAmount = 0;
    this.isDragging = false;
    this.startX = 0;
    this.scrollLeft = 0;
    
    this.init();
  }
  
  init() {
    // Setup navigation
    if (this.prevBtn) {
      this.prevBtn.addEventListener('click', () => this.scrollPrev());
    }
    
    if (this.nextBtn) {
      this.nextBtn.addEventListener('click', () => this.scrollNext());
    }
    
    // Track scroll position
    this.carousel.addEventListener('scroll', () => this.updateProgress());
    
    // Touch/drag support
    this.setupDragScroll();
    
    // Keyboard navigation
    this.carousel.addEventListener('keydown', (e) => this.handleKeyboard(e));
    
    // Initial update
    this.updateProgress();
    
    // Update on resize
    window.addEventListener('resize', () => this.updateProgress());
  }
  
  scrollPrev() {
    const itemWidth = this.carousel.querySelector('.steam-carousel-item')?.offsetWidth || 320;
    const gap = 24;
    const scrollAmount = itemWidth + gap;
    
    this.carousel.scrollBy({
      left: -scrollAmount,
      behavior: 'smooth'
    });
  }
  
  scrollNext() {
    const itemWidth = this.carousel.querySelector('.steam-carousel-item')?.offsetWidth || 320;
    const gap = 24;
    const scrollAmount = itemWidth + gap;
    
    this.carousel.scrollBy({
      left: scrollAmount,
      behavior: 'smooth'
    });
  }
  
  updateProgress() {
    const scrollLeft = this.carousel.scrollLeft;
    const scrollWidth = this.carousel.scrollWidth;
    const clientWidth = this.carousel.clientWidth;
    
    // Calculate progress percentage
    const maxScroll = scrollWidth - clientWidth;
    const progress = maxScroll > 0 ? (scrollLeft / maxScroll) * 100 : 0;
    
    // Update progress bar
    if (this.progressBar) {
      this.progressBar.style.width = `${progress}%`;
    }
    
    // Update button states
    if (this.prevBtn) {
      this.prevBtn.disabled = scrollLeft <= 0;
    }
    
    if (this.nextBtn) {
      this.nextBtn.disabled = scrollLeft >= maxScroll - 1;
    }
    
    // Update fade classes
    this.wrapper.classList.toggle('at-start', scrollLeft <= 0);
    this.wrapper.classList.toggle('at-end', scrollLeft >= maxScroll - 1);
  }
  
  setupDragScroll() {
    this.carousel.addEventListener('mousedown', (e) => {
      this.isDragging = true;
      this.startX = e.pageX - this.carousel.offsetLeft;
      this.scrollLeft = this.carousel.scrollLeft;
      this.carousel.style.cursor = 'grabbing';
      this.carousel.style.scrollBehavior = 'auto';
    });
    
    this.carousel.addEventListener('mouseleave', () => {
      this.isDragging = false;
      this.carousel.style.cursor = 'grab';
    });
    
    this.carousel.addEventListener('mouseup', () => {
      this.isDragging = false;
      this.carousel.style.cursor = 'grab';
      this.carousel.style.scrollBehavior = 'smooth';
    });
    
    this.carousel.addEventListener('mousemove', (e) => {
      if (!this.isDragging) return;
      e.preventDefault();
      const x = e.pageX - this.carousel.offsetLeft;
      const walk = (x - this.startX) * 2;
      this.carousel.scrollLeft = this.scrollLeft - walk;
    });
    
    // Touch support
    let touchStartX = 0;
    let touchScrollLeft = 0;
    
    this.carousel.addEventListener('touchstart', (e) => {
      touchStartX = e.touches[0].pageX;
      touchScrollLeft = this.carousel.scrollLeft;
    }, { passive: true });
    
    this.carousel.addEventListener('touchmove', (e) => {
      const touchX = e.touches[0].pageX;
      const walk = touchStartX - touchX;
      this.carousel.scrollLeft = touchScrollLeft + walk;
    }, { passive: true });
  }
  
  handleKeyboard(e) {
    if (e.key === 'ArrowLeft') {
      e.preventDefault();
      this.scrollPrev();
    } else if (e.key === 'ArrowRight') {
      e.preventDefault();
      this.scrollNext();
    } else if (e.key === 'Home') {
      e.preventDefault();
      this.carousel.scrollTo({ left: 0, behavior: 'smooth' });
    } else if (e.key === 'End') {
      e.preventDefault();
      this.carousel.scrollTo({ 
        left: this.carousel.scrollWidth, 
        behavior: 'smooth' 
      });
    }
  }
}

// ============================================
// CARD INTERACTIONS
// ============================================
class SteamCardController {
  constructor() {
    this.cards = [];
    this.init();
  }
  
  init() {
    // Find all steam cards
    this.cards = document.querySelectorAll('.steam-card, .steam-carousel-card');
    
    this.cards.forEach(card => {
      // Add click handler for play button
      const playBtn = card.querySelector('.steam-play-btn, .steam-carousel-card-play');
      if (playBtn) {
        playBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          this.playTrack(card);
        });
      }
      
      // Add click handler for card
      card.addEventListener('click', () => {
        this.openTrackDetails(card);
      });
      
      // Add action buttons handlers
      const actions = card.querySelectorAll('.steam-action-btn');
      actions.forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const action = btn.dataset.action;
          this.handleAction(action, card);
        });
      });
    });
  }
  
  playTrack(card) {
    const trackId = card.dataset.trackId;
    console.log('🎵 Playing track:', trackId);
    
    // Add playing state
    document.querySelectorAll('.steam-card, .steam-carousel-card').forEach(c => {
      c.classList.remove('playing');
    });
    card.classList.add('playing');
    
    // Update play button icon
    const playBtn = card.querySelector('.steam-play-btn i, .steam-carousel-card-play i');
    if (playBtn) {
      playBtn.className = 'fas fa-pause';
    }
    
    // Emit custom event
    window.dispatchEvent(new CustomEvent('trackPlay', {
      detail: { trackId, card }
    }));
  }
  
  openTrackDetails(card) {
    const trackId = card.dataset.trackId;
    console.log('ℹ️ Opening track details:', trackId);
    
    // Navigate to player page
    if (trackId) {
      window.location.href = `/player/${trackId}/`;
    }
  }
  
  handleAction(action, card) {
    const trackId = card.dataset.trackId;
    
    switch (action) {
      case 'like':
        console.log('❤️ Liked track:', trackId);
        this.toggleLike(card);
        break;
      case 'add-playlist':
        console.log('➕ Add to playlist:', trackId);
        this.showPlaylistMenu(card);
        break;
      case 'share':
        console.log('🔗 Share track:', trackId);
        this.shareTrack(card);
        break;
      case 'more':
        console.log('⋯ More options:', trackId);
        this.showMoreMenu(card);
        break;
      default:
        console.log('Unknown action:', action);
    }
  }
  
  toggleLike(card) {
    const likeBtn = card.querySelector('[data-action="like"] i');
    if (likeBtn) {
      const isLiked = likeBtn.classList.contains('fa-solid');
      likeBtn.className = isLiked ? 'far fa-heart' : 'fas fa-heart';
      
      // Add animation
      likeBtn.parentElement.style.transform = 'scale(1.3)';
      setTimeout(() => {
        likeBtn.parentElement.style.transform = '';
      }, 200);
    }
  }
  
  showPlaylistMenu(card) {
    // TODO: Implement playlist selector modal
    alert('Playlist menu coming soon!');
  }
  
  shareTrack(card) {
    const trackId = card.dataset.trackId;
    const url = `${window.location.origin}/player/${trackId}/`;
    
    if (navigator.share) {
      navigator.share({
        title: card.querySelector('.steam-card-title, .steam-carousel-card-title')?.textContent,
        url: url
      }).catch(err => console.log('Share failed:', err));
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(url).then(() => {
        alert('Link copied to clipboard!');
      });
    }
  }
  
  showMoreMenu(card) {
    // TODO: Implement context menu
    alert('More options coming soon!');
  }
}

// ============================================
// CATEGORY PILLS
// ============================================
class CategoryPillsController {
  constructor() {
    this.pills = [];
    this.init();
  }
  
  init() {
    this.pills = document.querySelectorAll('.steam-category-pill');
    
    this.pills.forEach(pill => {
      pill.addEventListener('click', () => {
        this.selectCategory(pill);
      });
    });
  }
  
  selectCategory(pill) {
    // Remove active from all
    this.pills.forEach(p => p.classList.remove('active'));
    
    // Add active to clicked
    pill.classList.add('active');
    
    // Get category
    const category = pill.dataset.category;
    console.log('📁 Selected category:', category);
    
    // Emit event
    window.dispatchEvent(new CustomEvent('categoryChange', {
      detail: { category }
    }));
  }
}

// ============================================
// FEATURED BANNER
// ============================================
class FeaturedBannerController {
  constructor() {
    this.banners = [];
    this.init();
  }
  
  init() {
    this.banners = document.querySelectorAll('.steam-featured');
    
    this.banners.forEach(banner => {
      // Play button
      const playBtn = banner.querySelector('.steam-featured-btn-primary');
      if (playBtn) {
        playBtn.addEventListener('click', () => {
          const trackId = banner.dataset.trackId;
          console.log('🎵 Playing featured track:', trackId);
          
          window.dispatchEvent(new CustomEvent('trackPlay', {
            detail: { trackId, banner }
          }));
        });
      }
      
      // Secondary button (usually "View Album" or "Add to Library")
      const secondaryBtn = banner.querySelector('.steam-featured-btn-secondary');
      if (secondaryBtn) {
        secondaryBtn.addEventListener('click', () => {
          const albumId = banner.dataset.albumId;
          console.log('💿 Opening album:', albumId);
          
          if (albumId) {
            window.location.href = `/album/${albumId}/`;
          }
        });
      }
    });
  }
}

// ============================================
// INITIALIZATION
// ============================================
class SteamUIController {
  constructor() {
    this.carousels = [];
    this.cardController = null;
    this.categoryController = null;
    this.featuredController = null;
    
    // Wait for DOM
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.init());
    } else {
      this.init();
    }
  }
  
  init() {
    // Initialize all carousels
    const carouselWrappers = document.querySelectorAll('.steam-carousel-wrapper');
    carouselWrappers.forEach(wrapper => {
      this.carousels.push(new SteamCarousel(wrapper));
    });
    
    // Initialize card controller
    this.cardController = new SteamCardController();
    
    // Initialize category pills
    this.categoryController = new CategoryPillsController();
    
    // Initialize featured banners
    this.featuredController = new FeaturedBannerController();
    
    console.log('✅ Steam UI initialized');
    console.log(`  - ${this.carousels.length} carousels`);
    console.log(`  - ${this.cardController.cards.length} cards`);
  }
}

// ============================================
// AUTO-INITIALIZE
// ============================================
window.SteamUI = new SteamUIController();

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    SteamCarousel,
    SteamCardController,
    CategoryPillsController,
    FeaturedBannerController,
    SteamUIController,
  };
}
