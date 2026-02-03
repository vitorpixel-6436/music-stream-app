/**
 * Recommendations Module
 * ======================
 * 
 * JavaScript module for ML-powered music recommendations.
 * Integrates with Django recommendation API.
 * 
 * Features:
 * - Personalized recommendations carousel
 * - Similar tracks display
 * - Top charts
 * - Continue listening
 * - Play tracking
 * 
 * Usage:
 *   const recs = new RecommendationManager();
 *   await recs.loadPersonalized();
 *   await recs.loadTopCharts('weekly');
 */

class RecommendationManager {
    constructor() {
        this.baseUrl = '/music/api';
        this.cache = new Map();
        this.cacheDuration = 3600000; // 1 hour in ms
    }

    // ========================================================================
    // CORE API METHODS
    // ========================================================================

    /**
     * Fetch personalized recommendations for current user
     * @param {number} limit - Number of recommendations
     * @returns {Promise<Array>} Array of track objects
     */
    async getPersonalized(limit = 20) {
        const cacheKey = `personalized_${limit}`;
        
        // Check cache
        if (this._isCached(cacheKey)) {
            return this.cache.get(cacheKey).data;
        }

        try {
            const response = await fetch(`${this.baseUrl}/recommendations/?limit=${limit}`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            
            if (data.status === 'success') {
                this._setCache(cacheKey, data.recommendations);
                return data.recommendations;
            } else {
                throw new Error(data.message || 'Failed to fetch recommendations');
            }
        } catch (error) {
            console.error('Personalized recommendations error:', error);
            return [];
        }
    }

    /**
     * Fetch tracks similar to given track
     * @param {string} trackId - UUID of track
     * @param {number} limit - Number of similar tracks
     * @returns {Promise<Array>} Array of similar tracks
     */
    async getSimilarTracks(trackId, limit = 10) {
        const cacheKey = `similar_${trackId}_${limit}`;
        
        if (this._isCached(cacheKey)) {
            return this.cache.get(cacheKey).data;
        }

        try {
            const response = await fetch(`${this.baseUrl}/track/${trackId}/similar/?limit=${limit}`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            
            if (data.status === 'success') {
                this._setCache(cacheKey, data.similar);
                return data.similar;
            } else {
                throw new Error(data.message || 'Failed to fetch similar tracks');
            }
        } catch (error) {
            console.error('Similar tracks error:', error);
            return [];
        }
    }

    /**
     * Fetch top charts
     * @param {string} period - 'weekly' or 'monthly'
     * @param {number} limit - Number of tracks
     * @returns {Promise<Array>} Array of top tracks
     */
    async getTopCharts(period = 'weekly', limit = 20) {
        const cacheKey = `charts_${period}_${limit}`;
        
        if (this._isCached(cacheKey)) {
            return this.cache.get(cacheKey).data;
        }

        try {
            const response = await fetch(`${this.baseUrl}/charts/?period=${period}&limit=${limit}`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            
            if (data.status === 'success') {
                this._setCache(cacheKey, data.charts);
                return data.charts;
            } else {
                throw new Error(data.message || 'Failed to fetch charts');
            }
        } catch (error) {
            console.error('Top charts error:', error);
            return [];
        }
    }

    /**
     * Fetch continue listening tracks
     * @param {number} limit - Number of tracks
     * @returns {Promise<Array>} Array of tracks to continue
     */
    async getContinueListening(limit = 10) {
        const cacheKey = `continue_${limit}`;
        
        if (this._isCached(cacheKey)) {
            return this.cache.get(cacheKey).data;
        }

        try {
            const response = await fetch(`${this.baseUrl}/continue-listening/?limit=${limit}`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            
            if (data.status === 'success') {
                this._setCache(cacheKey, data.tracks);
                return data.tracks;
            } else {
                throw new Error(data.message || 'Failed to fetch continue listening');
            }
        } catch (error) {
            console.error('Continue listening error:', error);
            return [];
        }
    }

    /**
     * Record a track play
     * @param {string} trackId - UUID of track
     * @param {object} playData - Play information
     * @returns {Promise<boolean>} Success status
     */
    async recordPlay(trackId, playData = {}) {
        try {
            const response = await fetch(`${this.baseUrl}/track/${trackId}/play/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this._getCsrfToken()
                },
                body: JSON.stringify({
                    duration: playData.duration || 0,
                    position: playData.position || 0,
                    source: playData.source || 'web',
                    device: playData.device || 'web'
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            return data.status === 'success';
        } catch (error) {
            console.error('Record play error:', error);
            return false;
        }
    }

    // ========================================================================
    // UI RENDERING
    // ========================================================================

    /**
     * Render recommendation carousel
     * @param {Array} tracks - Array of track objects
     * @param {HTMLElement} container - Container element
     * @param {string} title - Carousel title
     */
    renderCarousel(tracks, container, title = 'Recommendations') {
        if (!tracks || tracks.length === 0) {
            container.innerHTML = '<p class="no-recommendations">No recommendations available</p>';
            return;
        }

        const carouselHtml = `
            <div class="recommendation-carousel">
                <div class="carousel-header">
                    <h2 class="carousel-title">
                        <i class="fas fa-magic"></i>
                        ${title}
                    </h2>
                    <div class="carousel-controls">
                        <button class="carousel-btn carousel-prev" data-carousel="prev">
                            <i class="fas fa-chevron-left"></i>
                        </button>
                        <button class="carousel-btn carousel-next" data-carousel="next">
                            <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
                </div>
                <div class="carousel-track-wrapper">
                    <div class="carousel-track">
                        ${tracks.map(track => this._renderTrackCard(track)).join('')}
                    </div>
                </div>
            </div>
        `;

        container.innerHTML = carouselHtml;
        this._initCarouselControls(container);
    }

    /**
     * Render single track card
     * @param {object} track - Track object
     * @returns {string} HTML string
     * @private
     */
    _renderTrackCard(track) {
        const coverUrl = track.cover_url || '/static/music/img/default-cover.png';
        const artistName = track.artist?.name || 'Unknown Artist';
        const duration = this._formatDuration(track.duration);

        return `
            <div class="recommendation-card" data-track-id="${track.id}">
                <div class="card-image">
                    <img src="${coverUrl}" alt="${track.title}" loading="lazy">
                    <div class="card-overlay">
                        <button class="btn-play" data-action="play" data-track-id="${track.id}">
                            <i class="fas fa-play"></i>
                        </button>
                    </div>
                </div>
                <div class="card-content">
                    <h3 class="card-title" title="${track.title}">${track.title}</h3>
                    <p class="card-artist">${artistName}</p>
                    <div class="card-meta">
                        <span class="duration">
                            <i class="fas fa-clock"></i> ${duration}
                        </span>
                        ${track.play_count > 0 ? `
                            <span class="plays">
                                <i class="fas fa-headphones"></i> ${this._formatNumber(track.play_count)}
                            </span>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Initialize carousel navigation controls
     * @param {HTMLElement} container
     * @private
     */
    _initCarouselControls(container) {
        const track = container.querySelector('.carousel-track');
        const prevBtn = container.querySelector('[data-carousel="prev"]');
        const nextBtn = container.querySelector('[data-carousel="next"]');

        if (!track || !prevBtn || !nextBtn) return;

        let scrollPosition = 0;
        const scrollAmount = 300;

        prevBtn.addEventListener('click', () => {
            scrollPosition = Math.max(0, scrollPosition - scrollAmount);
            track.scrollTo({
                left: scrollPosition,
                behavior: 'smooth'
            });
        });

        nextBtn.addEventListener('click', () => {
            const maxScroll = track.scrollWidth - track.clientWidth;
            scrollPosition = Math.min(maxScroll, scrollPosition + scrollAmount);
            track.scrollTo({
                left: scrollPosition,
                behavior: 'smooth'
            });
        });

        // Update button states
        track.addEventListener('scroll', () => {
            scrollPosition = track.scrollLeft;
            prevBtn.disabled = scrollPosition === 0;
            nextBtn.disabled = scrollPosition >= track.scrollWidth - track.clientWidth - 10;
        });
    }

    // ========================================================================
    // HELPER METHODS
    // ========================================================================

    /**
     * Format duration from seconds to MM:SS
     * @param {number} seconds
     * @returns {string}
     * @private
     */
    _formatDuration(seconds) {
        if (!seconds) return '0:00';
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }

    /**
     * Format large numbers (1000 -> 1K)
     * @param {number} num
     * @returns {string}
     * @private
     */
    _formatNumber(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    }

    /**
     * Get CSRF token from cookies
     * @returns {string}
     * @private
     */
    _getCsrfToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }

    /**
     * Check if data is cached and valid
     * @param {string} key
     * @returns {boolean}
     * @private
     */
    _isCached(key) {
        if (!this.cache.has(key)) return false;
        
        const cached = this.cache.get(key);
        const isExpired = Date.now() - cached.timestamp > this.cacheDuration;
        
        if (isExpired) {
            this.cache.delete(key);
            return false;
        }
        
        return true;
    }

    /**
     * Set cache data
     * @param {string} key
     * @param {any} data
     * @private
     */
    _setCache(key, data) {
        this.cache.set(key, {
            data: data,
            timestamp: Date.now()
        });
    }

    /**
     * Clear all cache
     */
    clearCache() {
        this.cache.clear();
    }
}

// ============================================================================
// GLOBAL INSTANCE
// ============================================================================

// Create global instance for easy access
window.RecommendationManager = RecommendationManager;

// Auto-initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    window.recommendationManager = new RecommendationManager();
    console.log('Recommendation Manager initialized');
});
