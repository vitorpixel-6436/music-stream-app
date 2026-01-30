/**
 * DYNAMIC GLASS EFFECTS - Stage 1.2
 * 
 * Features:
 * - Scroll-based transparency (iOS Safari style)
 * - Particle effects behind glass elements
 * - Context-aware blur adjustments
 * - Smooth performance optimizations
 */

// ============================================
// CONFIGURATION
// ============================================
const GLASS_CONFIG = {
  // Scroll effects
  scrollThreshold: 50,
  maxBlur: 40,
  minBlur: 20,
  
  // Particles
  particleCount: 30,
  particleSpeed: 0.5,
  particleSize: { min: 2, max: 6 },
  
  // Performance
  useRAF: true,
  throttleDelay: 16, // ~60fps
};

// ============================================
// SCROLL-BASED TRANSPARENCY
// ============================================
class GlassScrollEffect {
  constructor() {
    this.elements = [];
    this.lastScroll = 0;
    this.ticking = false;
    
    this.init();
  }
  
  init() {
    // Find all elements with scroll effect
    this.elements = document.querySelectorAll('[data-glass-scroll]');
    
    if (this.elements.length === 0) return;
    
    // Add scroll listener
    window.addEventListener('scroll', () => this.requestTick(), { passive: true });
    
    // Initial update
    this.update();
  }
  
  requestTick() {
    if (!this.ticking) {
      requestAnimationFrame(() => this.update());
      this.ticking = true;
    }
  }
  
  update() {
    this.ticking = false;
    const scrollY = window.scrollY;
    
    this.elements.forEach(element => {
      const scrollEffect = element.dataset.glassScroll;
      
      switch (scrollEffect) {
        case 'fade':
          this.applyFadeEffect(element, scrollY);
          break;
        case 'blur':
          this.applyBlurEffect(element, scrollY);
          break;
        case 'elevate':
          this.applyElevateEffect(element, scrollY);
          break;
        default:
          this.applyDefaultEffect(element, scrollY);
      }
    });
    
    this.lastScroll = scrollY;
  }
  
  applyFadeEffect(element, scrollY) {
    // Increase opacity as user scrolls
    const progress = Math.min(scrollY / GLASS_CONFIG.scrollThreshold, 1);
    const opacity = 0.05 + (progress * 0.15); // 0.05 -> 0.20
    
    element.style.setProperty('--glass-opacity', opacity);
    element.style.background = `linear-gradient(135deg, rgba(255, 255, 255, ${opacity}) 0%, rgba(255, 255, 255, ${opacity * 0.5}) 100%)`;
  }
  
  applyBlurEffect(element, scrollY) {
    // Increase blur as user scrolls
    const progress = Math.min(scrollY / GLASS_CONFIG.scrollThreshold, 1);
    const blur = GLASS_CONFIG.minBlur + (progress * (GLASS_CONFIG.maxBlur - GLASS_CONFIG.minBlur));
    
    element.style.backdropFilter = `blur(${blur}px) saturate(180%)`;
    element.style.webkitBackdropFilter = `blur(${blur}px) saturate(180%)`;
  }
  
  applyElevateEffect(element, scrollY) {
    // Add shadow depth on scroll
    const progress = Math.min(scrollY / GLASS_CONFIG.scrollThreshold, 1);
    const shadowSize = 20 + (progress * 40); // 20px -> 60px
    const shadowOpacity = 0.3 + (progress * 0.3); // 0.3 -> 0.6
    
    element.style.boxShadow = `0 ${shadowSize}px ${shadowSize * 2}px rgba(0, 0, 0, ${shadowOpacity})`;
  }
  
  applyDefaultEffect(element, scrollY) {
    // Combined fade + blur
    this.applyFadeEffect(element, scrollY);
    this.applyBlurEffect(element, scrollY);
  }
}

// ============================================
// PARTICLE SYSTEM
// ============================================
class ParticleSystem {
  constructor(container) {
    this.container = container;
    this.canvas = null;
    this.ctx = null;
    this.particles = [];
    this.animationId = null;
    
    this.init();
  }
  
  init() {
    // Create canvas
    this.canvas = document.createElement('canvas');
    this.canvas.className = 'glass-particles-canvas';
    this.canvas.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: -1;
      opacity: 0.4;
    `;
    
    this.container.appendChild(this.canvas);
    this.ctx = this.canvas.getContext('2d');
    
    // Set canvas size
    this.resize();
    window.addEventListener('resize', () => this.resize());
    
    // Create particles
    this.createParticles();
    
    // Start animation
    this.animate();
  }
  
  resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }
  
  createParticles() {
    for (let i = 0; i < GLASS_CONFIG.particleCount; i++) {
      this.particles.push({
        x: Math.random() * this.canvas.width,
        y: Math.random() * this.canvas.height,
        size: Math.random() * (GLASS_CONFIG.particleSize.max - GLASS_CONFIG.particleSize.min) + GLASS_CONFIG.particleSize.min,
        speedX: (Math.random() - 0.5) * GLASS_CONFIG.particleSpeed,
        speedY: (Math.random() - 0.5) * GLASS_CONFIG.particleSpeed,
        opacity: Math.random() * 0.5 + 0.2,
        color: this.getRandomColor(),
      });
    }
  }
  
  getRandomColor() {
    const colors = [
      'rgba(227, 24, 55, ', // MSI Red
      'rgba(59, 130, 246, ', // Blue
      'rgba(139, 92, 246, ', // Purple
      'rgba(255, 255, 255, ', // White
    ];
    return colors[Math.floor(Math.random() * colors.length)];
  }
  
  animate() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    
    this.particles.forEach(particle => {
      // Update position
      particle.x += particle.speedX;
      particle.y += particle.speedY;
      
      // Wrap around edges
      if (particle.x < 0) particle.x = this.canvas.width;
      if (particle.x > this.canvas.width) particle.x = 0;
      if (particle.y < 0) particle.y = this.canvas.height;
      if (particle.y > this.canvas.height) particle.y = 0;
      
      // Draw particle
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
      this.ctx.fillStyle = particle.color + particle.opacity + ')';
      this.ctx.fill();
      
      // Add glow
      const gradient = this.ctx.createRadialGradient(
        particle.x, particle.y, 0,
        particle.x, particle.y, particle.size * 3
      );
      gradient.addColorStop(0, particle.color + (particle.opacity * 0.8) + ')');
      gradient.addColorStop(1, particle.color + '0)');
      
      this.ctx.fillStyle = gradient;
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, particle.size * 3, 0, Math.PI * 2);
      this.ctx.fill();
    });
    
    this.animationId = requestAnimationFrame(() => this.animate());
  }
  
  destroy() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
    if (this.canvas && this.canvas.parentNode) {
      this.canvas.parentNode.removeChild(this.canvas);
    }
  }
}

// ============================================
// CONTEXT-AWARE BLUR
// ============================================
class ContextAwareBlur {
  constructor() {
    this.elements = [];
    this.observer = null;
    
    this.init();
  }
  
  init() {
    // Find elements with context-aware blur
    this.elements = document.querySelectorAll('[data-glass-context]');
    
    if (this.elements.length === 0) return;
    
    // Create intersection observer
    this.observer = new IntersectionObserver(
      (entries) => this.handleIntersection(entries),
      {
        threshold: [0, 0.25, 0.5, 0.75, 1],
        rootMargin: '-50px'
      }
    );
    
    // Observe elements
    this.elements.forEach(el => this.observer.observe(el));
  }
  
  handleIntersection(entries) {
    entries.forEach(entry => {
      const element = entry.target;
      const visibility = entry.intersectionRatio;
      
      // Adjust blur based on visibility
      const blur = 20 + (visibility * 20); // 20px -> 40px
      const opacity = 0.05 + (visibility * 0.10); // 0.05 -> 0.15
      
      element.style.backdropFilter = `blur(${blur}px) saturate(${160 + (visibility * 20)}%)`;
      element.style.webkitBackdropFilter = `blur(${blur}px) saturate(${160 + (visibility * 20)}%)`;
      
      // Add entrance animation
      if (entry.isIntersecting && !element.classList.contains('glass-visible')) {
        element.classList.add('glass-visible');
        element.style.animation = 'glassFadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards';
      }
    });
  }
  
  destroy() {
    if (this.observer) {
      this.observer.disconnect();
    }
  }
}

// ============================================
// HOVER DEPTH EFFECT
// ============================================
class GlassHoverDepth {
  constructor() {
    this.elements = [];
    this.init();
  }
  
  init() {
    // Find hoverable glass elements
    this.elements = document.querySelectorAll('[data-glass-hover="depth"]');
    
    this.elements.forEach(element => {
      element.addEventListener('mouseenter', (e) => this.onMouseEnter(e));
      element.addEventListener('mousemove', (e) => this.onMouseMove(e));
      element.addEventListener('mouseleave', (e) => this.onMouseLeave(e));
    });
  }
  
  onMouseEnter(e) {
    const element = e.currentTarget;
    element.style.transition = 'transform 0.1s ease-out';
  }
  
  onMouseMove(e) {
    const element = e.currentTarget;
    const rect = element.getBoundingClientRect();
    
    // Calculate mouse position relative to element center
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    const deltaX = (e.clientX - centerX) / (rect.width / 2);
    const deltaY = (e.clientY - centerY) / (rect.height / 2);
    
    // Apply 3D transform
    const rotateX = deltaY * -10; // Max 10deg
    const rotateY = deltaX * 10;
    
    element.style.transform = `
      perspective(1000px)
      rotateX(${rotateX}deg)
      rotateY(${rotateY}deg)
      translateZ(10px)
      scale(1.02)
    `;
    
    // Update shadow based on tilt
    const shadowX = deltaX * 20;
    const shadowY = deltaY * 20;
    element.style.boxShadow = `
      ${shadowX}px ${shadowY + 20}px 60px rgba(0, 0, 0, 0.5),
      inset 0 1px 0 rgba(255, 255, 255, 0.2)
    `;
  }
  
  onMouseLeave(e) {
    const element = e.currentTarget;
    element.style.transition = 'transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s cubic-bezier(0.16, 1, 0.3, 1)';
    element.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px) scale(1)';
    element.style.boxShadow = '';
  }
}

// ============================================
// PERFORMANCE MONITOR
// ============================================
class GlassPerformanceMonitor {
  constructor() {
    this.fps = 60;
    this.lastTime = performance.now();
    this.frames = 0;
    this.checkInterval = 1000; // Check every second
    
    this.monitor();
  }
  
  monitor() {
    const currentTime = performance.now();
    this.frames++;
    
    if (currentTime >= this.lastTime + this.checkInterval) {
      this.fps = Math.round((this.frames * 1000) / (currentTime - this.lastTime));
      this.frames = 0;
      this.lastTime = currentTime;
      
      // Adjust quality based on FPS
      this.adjustQuality();
    }
    
    requestAnimationFrame(() => this.monitor());
  }
  
  adjustQuality() {
    // Reduce effects if FPS drops below 45
    if (this.fps < 45) {
      document.documentElement.classList.add('glass-low-performance');
      console.warn('⚠️ Glass effects reduced due to low performance');
    } else {
      document.documentElement.classList.remove('glass-low-performance');
    }
  }
}

// ============================================
// INITIALIZATION
// ============================================
class GlassDynamics {
  constructor() {
    this.scrollEffect = null;
    this.particles = null;
    this.contextBlur = null;
    this.hoverDepth = null;
    this.perfMonitor = null;
    
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.init());
    } else {
      this.init();
    }
  }
  
  init() {
    // Check if user prefers reduced motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    if (prefersReducedMotion) {
      console.log('ℹ️ Reduced motion detected, skipping dynamic effects');
      return;
    }
    
    // Initialize all systems
    this.scrollEffect = new GlassScrollEffect();
    this.contextBlur = new ContextAwareBlur();
    this.hoverDepth = new GlassHoverDepth();
    
    // Initialize particles (only on desktop)
    if (window.innerWidth >= 1024) {
      const particleContainer = document.querySelector('[data-glass-particles]') || document.body;
      this.particles = new ParticleSystem(particleContainer);
    }
    
    // Initialize performance monitor
    if (window.location.search.includes('debug=glass')) {
      this.perfMonitor = new GlassPerformanceMonitor();
    }
    
    console.log('✅ Glass Dynamics initialized');
  }
  
  destroy() {
    if (this.particles) {
      this.particles.destroy();
    }
    if (this.contextBlur) {
      this.contextBlur.destroy();
    }
  }
}

// ============================================
// AUTO-INITIALIZE
// ============================================
window.GlassDynamics = new GlassDynamics();

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    GlassDynamics,
    GlassScrollEffect,
    ParticleSystem,
    ContextAwareBlur,
    GlassHoverDepth,
  };
}
