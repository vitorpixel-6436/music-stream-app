/**
 * Recommendations JavaScript Module
 * ==================================
 * 
 * Handles ML-powered music recommendations:
 * - Personalized recommendations
 * - Similar tracks
 * - Top charts
 * - Continue listening
 * - Play tracking
 * 
 * Uses REST API endpoints from recommendation_views.py
 */

const Recommendations = {
    /**
     * Configuration
     */
    config: {
        apiBaseUrl: '/music/api',
        refreshInterval: 60000, // 1 minute
        cacheTimeout: 300000, // 5 minutes
        defaultLimit: 20,
    },

    /**
     * Cache storage
     */
    cache: {
        personalized: null,
        charts: null,
        continue: null,
        lastFetch: {},
    },

    /**
     * Initialize recommendations
     */
    init() {
        console.log('[Recommendations] Initializing...');
        
        // Load personalized recommendations on page load
        if (this.isUserAuthenticated()) {
            this.loadPersonalizedRecommendations();
            this.loadContinueListening();
        }
        
        // Load public content
        this.loadTopCharts();
        
        // Setup auto-refresh
        this.setupAutoRefresh();
        
        // Setup play tracking
        this.setupPlayTracking();
    },

    /**
     * Check if user is authenticated
     */
    isUserAuthenticated() {
        // Check if user meta tag exists
        const userMeta = document.querySelector('meta[name="user-authenticated"]');
        return userMeta && userMeta.content === 'true';
    },

    /**
     * Load personalized recommendations
     */
    async loadPersonalizedRecommendations(limit = 20) {
        const container = document.getElementById('personalized-recommendations');
        if (!container) return;

        // Check cache
        if (this.isCacheValid('personalized')) {
            this.renderRecommendations(this.cache.personalized, container);
            return;
        }

        // Show loading state
        this.showLoading(container);

        try {
            const response = await fetch(
                `${this.config.apiBaseUrl}/recommendations/?limit=${limit}`
            );

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();

            if (data.status === 'success') {
                // Cache results
                this.cache.personalized = data.recommendations;
                this.cache.lastFetch.personalized = Date.now();

                // Render
                this.renderRecommendations(data.recommendations, container);
            } else {
                this.showError(container, data.message || 'Failed to load recommendations');
            }
        } catch (error) {
            console.error('[Recommendations] Error loading personalized:', error);
            this.showError(container, 'Failed to load recommendations');
        }
    },

    /**
     * Load similar tracks for given track ID
     */
    async loadSimilarTracks(trackId, limit = 10) {
        const container = document.getElementById(`similar-tracks-${trackId}`);
        if (!container) return;

        // Show loading
        this.showLoading(container);

        try {
            const response = await fetch(
                `${this.config.apiBaseUrl}/track/${trackId}/similar/?limit=${limit}`
            );

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();

            if (data.status === 'success') {
                this.renderRecommendations(data.similar, container);
            } else {
                this.showError(container, data.message);
            }
        } catch (error) {
            console.error('[Recommendations] Error loading similar tracks:', error);
            this.showError(container, 'Failed to load similar tracks');
        }
    },

    /**
     * Load top charts
     */
    async loadTopCharts(period = 'weekly', limit = 20) {
        const container = document.getElementById('top-charts');
        if (!container) return;

        // Check cache
        const cacheKey = `charts_${period}`;
        if (this.isCacheValid(cacheKey)) {
            this.renderRecommendations(this.cache[cacheKey], container);
            return;
        }

        // Show loading
        this.showLoading(container);

        try {
            const response = await fetch(
                `${this.config.apiBaseUrl}/charts/?period=${period}&limit=${limit}`
            );

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();

            if (data.status === 'success') {
                // Cache
                this.cache[cacheKey] = data.charts;
                this.cache.lastFetch[cacheKey] = Date.now();

                // Render
                this.renderRecommendations(data.charts, container);
            } else {
                this.showError(container, data.message);
            }
        } catch (error) {
            console.error('[Recommendations] Error loading charts:', error);
            this.showError(container, 'Failed to load charts');
        }
    },

    /**
     * Load continue listening
     */
    async loadContinueListening(limit = 10) {
        const container = document.getElementById('continue-listening');
        if (!container) return;

        // Check cache
        if (this.isCacheValid('continue')) {
            this.renderRecommendations(this.cache.continue, container);
            return;
        }

        // Show loading
        this.showLoading(container);

        try {
            const response = await fetch(
                `${this.config.apiBaseUrl}/continue-listening/?limit=${limit}`
            );

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();

            if (data.status === 'success') {
                // Cache
                this.cache.continue = data.tracks;
                this.cache.lastFetch.continue = Date.now();

                // Render
                this.renderRecommendations(data.tracks, container);
            } else {
                this.showError(container, data.message);
            }
        } catch (error) {
            console.error('[Recommendations] Error loading continue listening:', error);
            this.showError(container, 'Failed to load continue listening');
        }
    },

    /**
     * Render recommendations as cards
     */
    renderRecommendations(tracks, container) {
        if (!tracks || tracks.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-music"></i>
                    <p>No recommendations available yet</p>
                    <small>Listen to some music to get personalized recommendations</small>
                </div>
            `;
            return;
        }

        // Create carousel wrapper
        const carousel = document.createElement('div');
        carousel.className = 'recommendation-carousel';

        tracks.forEach((track, index) => {
            const card = this.createTrackCard(track, index);
            carousel.appendChild(card);
        });

        // Clear and append
        container.innerHTML = '';
        container.appendChild(carousel);

        // Initialize carousel scrolling if needed
        this.initializeCarouselScroll(carousel);
    },

    /**
     * Create track card HTML
     */
    createTrackCard(track, index) {
        const card = document.createElement('div');
        card.className = 'recommendation-card';
        card.dataset.trackId = track.id;

        // Cover image
        const coverUrl = track.cover_url || '/static/music/img/default-cover.png';

        card.innerHTML = `
            <div class="card-cover">
                <img src="${coverUrl}" alt="${this.escapeHtml(track.title)}" loading="lazy">
                <div class="card-overlay">
                    <button class="play-btn" data-track-id="${track.id}">
                        <i class="fas fa-play"></i>
                    </button>
                </div>
            </div>
            <div class="card-info">
                <h4 class="card-title">${this.escapeHtml(track.title)}</h4>
                <p class="card-artist">${this.escapeHtml(track.artist.name)}</p>
                <div class="card-meta">
                    <span class="duration">${this.formatDuration(track.duration)}</span>
                    ${track.play_count > 0 ? `<span class="plays">${track.play_count} plays</span>` : ''}
                </div>
            </div>
        `;

        // Add click handler for play button
        const playBtn = card.querySelector('.play-btn');
        playBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.playTrack(track);
        });

        // Add click handler for card
        card.addEventListener('click', () => {
            window.location.href = `/music/player/${track.id}/`;
        });

        return card;
    },

    /**
     * Record play event
     */
    async recordPlay(trackId, duration, position, source = 'recommendations') {
        if (!this.isUserAuthenticated()) return;

        try {
            const response = await fetch(
                `${this.config.apiBaseUrl}/track/${trackId}/play/`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        duration: duration,
                        position: position,
                        source: source,
                        device: 'web',
                    }),
                }
            );

            const data = await response.json();
            
            if (data.status === 'success') {
                console.log('[Recommendations] Play recorded:', data.play_id);
            }
        } catch (error) {
            console.error('[Recommendations] Error recording play:', error);
        }
    },

    /**
     * Play track (integrate with player)
     */
    playTrack(track) {
        // Dispatch custom event for player to handle
        const event = new CustomEvent('playTrack', {
            detail: { track: track }
        });
        document.dispatchEvent(event);

        console.log('[Recommendations] Playing track:', track.title);
    },

    /**
     * Setup play tracking
     */
    setupPlayTracking() {
        // Listen for track end events from player
        document.addEventListener('trackEnded', (e) => {
            const { trackId, duration, position } = e.detail;
            this.recordPlay(trackId, duration, position);
        });

        // Listen for track skip events
        document.addEventListener('trackSkipped', (e) => {
            const { trackId, duration, position } = e.detail;
            this.recordPlay(trackId, duration, position);
        });
    },

    /**
     * Setup auto-refresh
     */
    setupAutoRefresh() {
        setInterval(() => {
            // Refresh if user is authenticated
            if (this.isUserAuthenticated()) {
                // Only refresh if cache is expired
                if (!this.isCacheValid('personalized')) {
                    this.loadPersonalizedRecommendations();
                }
                if (!this.isCacheValid('continue')) {
                    this.loadContinueListening();
                }
            }

            // Refresh charts
            if (!this.isCacheValid('charts_weekly')) {
                this.loadTopCharts('weekly');
            }
        }, this.config.refreshInterval);
    },

    /**
     * Initialize carousel horizontal scroll
     */
    initializeCarouselScroll(carousel) {
        let isDown = false;
        let startX;
        let scrollLeft;

        carousel.addEventListener('mousedown', (e) => {
            isDown = true;
            carousel.classList.add('active');
            startX = e.pageX - carousel.offsetLeft;
            scrollLeft = carousel.scrollLeft;
        });

        carousel.addEventListener('mouseleave', () => {
            isDown = false;
            carousel.classList.remove('active');
        });

        carousel.addEventListener('mouseup', () => {
            isDown = false;
            carousel.classList.remove('active');
        });

        carousel.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - carousel.offsetLeft;
            const walk = (x - startX) * 2;
            carousel.scrollLeft = scrollLeft - walk;
        });
    },

    /**
     * Show loading state
     */
    showLoading(container) {
        container.innerHTML = `
            <div class="loading-state">
                <div class="spinner"></div>
                <p>Loading recommendations...</p>
            </div>
        `;
    },

    /**
     * Show error state
     */
    showError(container, message) {
        container.innerHTML = `
            <div class="error-state">
                <i class="fas fa-exclamation-circle"></i>
                <p>${this.escapeHtml(message)}</p>
                <button onclick="location.reload()">Retry</button>
            </div>
        `;
    },

    /**
     * Check if cache is valid
     */
    isCacheValid(key) {
        const lastFetch = this.cache.lastFetch[key];
        if (!lastFetch) return false;

        const age = Date.now() - lastFetch;
        return age < this.config.cacheTimeout && this.cache[key];
    },

    /**
     * Format duration (seconds to MM:SS)
     */
    formatDuration(seconds) {
        if (!seconds) return '0:00';

        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    },

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },
};

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => Recommendations.init());
} else {
    Recommendations.init();
}

// Export for use in other modules
window.Recommendations = Recommendations;
