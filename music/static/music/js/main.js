/**
 * Music Stream App - Main JavaScript
 * Interactive UI enhancements and utilities
 */

// ========================================
// GLOBAL UTILITIES
// ========================================

// Show Toast Notification
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    const colors = {
        'success': 'glass-red',
        'error': 'glass-dark border border-red-500',
        'info': 'glass',
        'warning': 'glass-dark border border-yellow-500'
    };
    
    toast.className = `fixed bottom-8 right-8 ${colors[type] || colors.info} px-6 py-4 rounded-2xl shadow-2xl slide-up z-[100] max-w-sm`;
    toast.innerHTML = `
        <div class="flex items-center gap-4">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} text-2xl ${type === 'success' ? 'text-green-400' : type === 'error' ? 'text-red-400' : 'text-blue-400'}"></i>
            <div class="flex-1">
                <div class="font-semibold text-sm">${message}</div>
            </div>
            <button onclick="this.parentElement.parentElement.remove()" class="text-white/40 hover:text-white transition-colors">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-hide
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(100px)';
        setTimeout(() => toast.remove(), 500);
    }, duration);
}

// Format Time (MM:SS)
function formatTime(seconds) {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Format File Size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// ========================================
// GLOBAL KEYBOARD SHORTCUTS
// ========================================

document.addEventListener('keydown', (e) => {
    // Don't trigger if user is typing in input
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    
    // Space - Play/Pause
    if (e.code === 'Space') {
        e.preventDefault();
        const audio = document.getElementById('audio-player');
        if (audio) {
            if (audio.paused) {
                audio.play();
            } else {
                audio.pause();
            }
        }
    }
    
    // M - Mute/Unmute
    if (e.code === 'KeyM') {
        e.preventDefault();
        const audio = document.getElementById('audio-player');
        if (audio) {
            audio.muted = !audio.muted;
        }
    }
    
    // Arrow Left - Seek -5s
    if (e.code === 'ArrowLeft') {
        e.preventDefault();
        const audio = document.getElementById('audio-player');
        if (audio) {
            audio.currentTime = Math.max(0, audio.currentTime - 5);
        }
    }
    
    // Arrow Right - Seek +5s
    if (e.code === 'ArrowRight') {
        e.preventDefault();
        const audio = document.getElementById('audio-player');
        if (audio) {
            audio.currentTime = Math.min(audio.duration || 0, audio.currentTime + 5);
        }
    }
    
    // Escape - Close modals/overlays
    if (e.code === 'Escape') {
        // Add modal close logic here
    }
});

// ========================================
// SCROLL ANIMATIONS
// ========================================

// Fade in elements on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all elements with data-animate attribute
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('[data-animate]');
    animatedElements.forEach(el => observer.observe(el));
});

// ========================================
// CARD PARALLAX EFFECT
// ========================================

function initCardParallax() {
    const cards = document.querySelectorAll('.track-card');
    
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px) scale(1.03)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
        });
    });
}

// Initialize on DOM load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCardParallax);
} else {
    initCardParallax();
}

// ========================================
// SMOOTH SCROLL
// ========================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href === '#') return;
        
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ========================================
// LOCAL STORAGE UTILITIES
// ========================================

const Storage = {
    set: (key, value) => {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.warn('localStorage not available:', e);
        }
    },
    
    get: (key, defaultValue = null) => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (e) {
            console.warn('localStorage not available:', e);
            return defaultValue;
        }
    },
    
    remove: (key) => {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.warn('localStorage not available:', e);
        }
    }
};

// ========================================
// VOLUME PERSISTENCE
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    const audio = document.getElementById('audio-player');
    if (audio) {
        // Restore saved volume
        const savedVolume = Storage.get('playerVolume', 0.7);
        audio.volume = savedVolume;
        
        const volumeSlider = document.getElementById('volume-slider');
        if (volumeSlider) {
            volumeSlider.value = savedVolume * 100;
        }
        
        // Save volume on change
        audio.addEventListener('volumechange', () => {
            Storage.set('playerVolume', audio.volume);
        });
    }
});

// ========================================
// SEARCH DEBOUNCE
// ========================================

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ========================================
// DYNAMIC GRID RESIZE
// ========================================

function adjustGridColumns() {
    const grids = document.querySelectorAll('.track-grid, [class*="grid-cols"]');
    const width = window.innerWidth;
    
    // This is handled by Tailwind responsive classes
    // but you can add custom logic here if needed
}

window.addEventListener('resize', debounce(adjustGridColumns, 250));

// ========================================
// EXPORT UTILITIES
// ========================================

window.MusicStreamApp = {
    showToast,
    formatTime,
    formatFileSize,
    Storage
};

console.log('%c🎵 Music Stream App Loaded', 'color: #dc2626; font-size: 16px; font-weight: bold;');
console.log('%cKeyboard Shortcuts:', 'color: #9ca3af; font-size: 12px;');
console.log('%c  Space  - Play/Pause', 'color: #6b7280; font-size: 11px;');
console.log('%c  M      - Mute/Unmute', 'color: #6b7280; font-size: 11px;');
console.log('%c  ←/→    - Seek ±5s', 'color: #6b7280; font-size: 11px;');
