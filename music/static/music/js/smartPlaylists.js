/**
 * Smart Playlists Module
 * Generates automatic playlists based on listening history and user preferences
 * Features: Most Played, Recent, Favorites, Genre-based
 */

class SmartPlaylists {
  constructor() {
    this.db = null;
    this.initialized = false;
    this.playlistTypes = ['mostPlayed', 'recent', 'favorites', 'genre'];
    this.init();
  }

  init() {
    // Initialize IndexedDB for smart playlists
    const request = indexedDB.open('musicStreamDB', 1);
    
    request.onerror = () => {
      console.error('Failed to open IndexedDB');
    };
    
    request.onsuccess = (e) => {
      this.db = e.target.result;
      this.initialized = true;
      this.setupStores();
    };
    
    request.onupgradeneeded = (e) => {
      const db = e.target.result;
      
      if (!db.objectStoreNames.contains('tracks')) {
        db.createObjectStore('tracks', { keyPath: 'id' });
      }
      if (!db.objectStoreNames.contains('playlists')) {
        db.createObjectStore('playlists', { keyPath: 'id' });
      }
      if (!db.objectStoreNames.contains('listening_history')) {
        db.createObjectStore('listening_history', { keyPath: 'id', autoIncrement: true });
      }
    };
  }

  setupStores() {
    // Create indexes for efficient queries
    const tx = this.db.transaction(['listening_history'], 'readwrite');
    const store = tx.objectStore('listening_history');
    
    if (!store.indexNames.contains('timestamp')) {
      store.createIndex('timestamp', 'timestamp', { unique: false });
    }
    if (!store.indexNames.contains('trackId')) {
      store.createIndex('trackId', 'trackId', { unique: false });
    }
  }

  // Track listening history
  trackListen(trackId, trackData) {
    if (!this.initialized) return;
    
    const tx = this.db.transaction(['listening_history'], 'readwrite');
    const store = tx.objectStore('listening_history');
    
    store.add({
      trackId: trackId,
      trackData: trackData,
      timestamp: Date.now(),
      playCount: 1
    });
  }

  // Generate Most Played Playlist
  async generateMostPlayed(limit = 50) {
    if (!this.initialized) return [];
    
    const tx = this.db.transaction(['listening_history'], 'readonly');
    const store = tx.objectStore('listening_history');
    const allItems = await this.getAllFromStore(store);
    
    const trackMap = {};
    allItems.forEach(item => {
      if (!trackMap[item.trackId]) {
        trackMap[item.trackId] = {
          ...item.trackData,
          playCount: 0
        };
      }
      trackMap[item.trackId].playCount++;
    });
    
    return Object.values(trackMap)
      .sort((a, b) => b.playCount - a.playCount)
      .slice(0, limit);
  }

  // Generate Recent Playlist
  async generateRecent(limit = 50) {
    if (!this.initialized) return [];
    
    const tx = this.db.transaction(['listening_history'], 'readonly');
    const store = tx.objectStore('listening_history');
    const allItems = await this.getAllFromStore(store);
    
    const uniqueTracks = {};
    allItems.reverse().forEach(item => {
      if (!uniqueTracks[item.trackId]) {
        uniqueTracks[item.trackId] = {
          ...item.trackData,
          lastPlayed: item.timestamp
        };
      }
    });
    
    return Object.values(uniqueTracks)
      .sort((a, b) => b.lastPlayed - a.lastPlayed)
      .slice(0, limit);
  }

  // Generate Favorites Playlist
  async generateFavorites() {
    if (!this.initialized) return [];
    
    const tx = this.db.transaction(['tracks'], 'readonly');
    const store = tx.objectStore('tracks');
    const allTracks = await this.getAllFromStore(store);
    
    return allTracks.filter(track => track.isFavorite === true);
  }

  // Generate Genre-based Playlist
  async generateByGenre(genre, limit = 50) {
    if (!this.initialized) return [];
    
    const tx = this.db.transaction(['tracks'], 'readonly');
    const store = tx.objectStore('tracks');
    const allTracks = await this.getAllFromStore(store);
    
    return allTracks
      .filter(track => track.genre === genre)
      .slice(0, limit);
  }

  // Helper method to get all items from store
  getAllFromStore(store) {
    return new Promise((resolve, reject) => {
      const request = store.getAll();
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  // Save smart playlist
  async savePlaylist(name, tracks, type) {
    if (!this.initialized) return false;
    
    const tx = this.db.transaction(['playlists'], 'readwrite');
    const store = tx.objectStore('playlists');
    
    return new Promise((resolve, reject) => {
      const request = store.add({
        id: Date.now(),
        name: name,
        tracks: tracks,
        type: type,
        created: new Date(),
        isSmart: true
      });
      request.onsuccess = () => resolve(true);
      request.onerror = () => reject(false);
    });
  }

  // Get all smart playlists
  async getAllPlaylists() {
    if (!this.initialized) return [];
    
    const tx = this.db.transaction(['playlists'], 'readonly');
    const store = tx.objectStore('playlists');
    
    return this.getAllFromStore(store);
  }

  // Delete smart playlist
  async deletePlaylist(playlistId) {
    if (!this.initialized) return false;
    
    const tx = this.db.transaction(['playlists'], 'readwrite');
    const store = tx.objectStore('playlists');
    
    return new Promise((resolve, reject) => {
      const request = store.delete(playlistId);
      request.onsuccess = () => resolve(true);
      request.onerror = () => reject(false);
    });
  }
}

// Global instance
window.smartPlaylists = null;

// Initialize smart playlists
function initSmartPlaylists() {
  if (window.smartPlaylists) return;
  window.smartPlaylists = new SmartPlaylists();
}

// Export for external use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SmartPlaylists;
}
