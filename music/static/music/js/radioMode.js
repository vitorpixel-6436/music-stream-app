/**
 * Radio Mode Module
 * Provides infinite playback based on genre, artist, or user preferences
 * Features: Genre-based queue, similar tracks, recommendations
 */

class RadioMode {
  constructor() {
    this.isRadioActive = false;
    this.currentGenre = null;
    this.currentArtist = null;
    this.radioQueue = [];
    this.playedTracks = new Set();
    this.queueIndex = 0;
    this.similarityThreshold = 0.6; // Similarity threshold for track recommendations
    this.init();
  }

  init() {
    // Set up event listeners
    document.addEventListener('trackEnded', () => this.nextTrack());
    document.addEventListener('radioStart', (e) => this.startRadio(e.detail));
    document.addEventListener('radioStop', () => this.stopRadio());
  }

  // Start radio mode
  async startRadio(options = {}) {
    const { genre = null, artist = null, tracks = [] } = options;
    
    this.isRadioActive = true;
    this.currentGenre = genre;
    this.currentArtist = artist;
    this.radioQueue = [];
    this.playedTracks = new Set();
    
    // Initialize queue with seed tracks
    if (tracks && tracks.length > 0) {
      this.radioQueue = [...tracks];
    } else if (genre) {
      await this.initQueueByGenre(genre);
    } else if (artist) {
      await this.initQueueByArtist(artist);
    }
    
    console.log('Radio mode started with', this.radioQueue.length, 'initial tracks');
    return this.radioQueue.length > 0;
  }

  // Initialize queue based on genre
  async initQueueByGenre(genre) {
    try {
      const response = await fetch(`/api/tracks?genre=${encodeURIComponent(genre)}&limit=50`);
      if (!response.ok) throw new Error('Failed to fetch genre tracks');
      
      const data = await response.json();
      this.radioQueue = data.tracks || [];
      this.radioQueue = this.radioQueue.sort(() => Math.random() - 0.5); // Shuffle
    } catch (error) {
      console.error('Error initializing radio queue by genre:', error);
    }
  }

  // Initialize queue based on artist
  async initQueueByArtist(artist) {
    try {
      const response = await fetch(`/api/tracks?artist=${encodeURIComponent(artist)}&limit=30`);
      if (!response.ok) throw new Error('Failed to fetch artist tracks');
      
      const data = await response.json();
      this.radioQueue = data.tracks || [];
      this.radioQueue = this.radioQueue.sort(() => Math.random() - 0.5); // Shuffle
    } catch (error) {
      console.error('Error initializing radio queue by artist:', error);
    }
  }

  // Get next track for radio playback
  async getNextTrack() {
    if (!this.isRadioActive) return null;
    
    // If queue is running low, fetch more tracks
    if (this.queueIndex >= this.radioQueue.length - 10) {
      await this.refillQueue();
    }
    
    if (this.queueIndex >= this.radioQueue.length) {
      return null;
    }
    
    const track = this.radioQueue[this.queueIndex];
    this.playedTracks.add(track.id);
    this.queueIndex++;
    
    return track;
  }

  // Refill queue with similar tracks
  async refillQueue() {
    try {
      if (this.currentGenre) {
        const response = await fetch(`/api/tracks?genre=${encodeURIComponent(this.currentGenre)}&limit=30&exclude=${Array.from(this.playedTracks).join(',')}`);
        if (response.ok) {
          const data = await response.json();
          const newTracks = (data.tracks || []).filter(t => !this.playedTracks.has(t.id));
          this.radioQueue.push(...newTracks);
        }
      } else if (this.currentArtist) {
        const response = await fetch(`/api/similar-artists?artist=${encodeURIComponent(this.currentArtist)}&limit=30`);
        if (response.ok) {
          const data = await response.json();
          const newTracks = (data.tracks || []).filter(t => !this.playedTracks.has(t.id));
          this.radioQueue.push(...newTracks);
        }
      }
    } catch (error) {
      console.error('Error refilling radio queue:', error);
    }
  }

  // Get similar tracks
  async getSimilarTracks(trackId, limit = 10) {
    try {
      const response = await fetch(`/api/similar-tracks?trackId=${trackId}&limit=${limit}`);
      if (!response.ok) throw new Error('Failed to fetch similar tracks');
      
      const data = await response.json();
      return data.tracks || [];
    } catch (error) {
      console.error('Error fetching similar tracks:', error);
      return [];
    }
  }

  // Track similarity based on features
  calculateSimilarity(track1, track2) {
    let similarity = 0;
    let factors = 0;
    
    // Genre similarity
    if (track1.genre && track2.genre) {
      similarity += track1.genre === track2.genre ? 1 : 0.3;
      factors++;
    }
    
    // Artist similarity (same artist or collaborators)
    if (track1.artist && track2.artist) {
      similarity += track1.artist === track2.artist ? 1 : 0.2;
      factors++;
    }
    
    // Tempo similarity (if available)
    if (track1.tempo && track2.tempo) {
      const tempoDiff = Math.abs(track1.tempo - track2.tempo) / Math.max(track1.tempo, track2.tempo);
      similarity += (1 - tempoDiff);
      factors++;
    }
    
    // Energy similarity (if available)
    if (track1.energy && track2.energy) {
      const energyDiff = Math.abs(track1.energy - track2.energy);
      similarity += (1 - energyDiff);
      factors++;
    }
    
    return factors > 0 ? similarity / factors : 0;
  }

  // Get recommendations based on current track
  async getRecommendations(currentTrack, limit = 5) {
    const similarTracks = await this.getSimilarTracks(currentTrack.id, limit * 2);
    
    // Filter and score by similarity
    const scored = similarTracks
      .filter(t => !this.playedTracks.has(t.id))
      .map(t => ({
        ...t,
        score: this.calculateSimilarity(currentTrack, t)
      }))
      .sort((a, b) => b.score - a.score);
    
    return scored.slice(0, limit);
  }

  // Next track event handler
  async nextTrack() {
    if (!this.isRadioActive) return;
    
    const nextTrack = await this.getNextTrack();
    if (nextTrack) {
      const event = new CustomEvent('playTrack', { detail: { track: nextTrack, autoPlay: true } });
      document.dispatchEvent(event);
    }
  }

  // Stop radio mode
  stopRadio() {
    this.isRadioActive = false;
    this.radioQueue = [];
    this.playedTracks.clear();
    this.queueIndex = 0;
    console.log('Radio mode stopped');
  }

  // Get radio status
  getStatus() {
    return {
      isActive: this.isRadioActive,
      genre: this.currentGenre,
      artist: this.currentArtist,
      queueLength: this.radioQueue.length,
      queueIndex: this.queueIndex,
      playedCount: this.playedTracks.size
    };
  }

  // Change radio mode parameters
  async changeRadioMode(options = {}) {
    if (this.isRadioActive) {
      this.stopRadio();
    }
    await this.startRadio(options);
  }
}

// Global instance
window.radioMode = null;

// Initialize radio mode
function initRadioMode() {
  if (window.radioMode) return;
  window.radioMode = new RadioMode();
}

// Export for external use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = RadioMode;
}
