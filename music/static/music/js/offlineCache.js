/**
 * Offline Caching Module
 * Uses IndexedDB to cache tracks, playlists, and metadata for offline access
 * Features: Track caching, smart eviction, sync tracking
 */

class OfflineCache {
  constructor(dbName = 'musicStreamDB', version = 1) {
    this.dbName = dbName;
    this.version = version;
    this.db = null;
    this.initialized = false;
    this.maxCacheSize = 500 * 1024 * 1024; // 500MB default
    this.currentCacheSize = 0;
    this.init();
  }

  init() {
    const request = indexedDB.open(this.dbName, this.version);
    
    request.onerror = () => {
      console.error('Failed to open offline cache database');
    };
    
    request.onsuccess = (e) => {
      this.db = e.target.result;
      this.initialized = true;
      this.calculateCacheSize();
      console.log('Offline cache initialized');
    };
    
    request.onupgradeneeded = (e) => {
      const db = e.target.result;
      
      // Create object stores
      if (!db.objectStoreNames.contains('cached_tracks')) {
        const trackStore = db.createObjectStore('cached_tracks', { keyPath: 'id' });
        trackStore.createIndex('cached_date', 'cached_date');
        trackStore.createIndex('access_count', 'access_count');
      }
      
      if (!db.objectStoreNames.contains('cached_metadata')) {
        db.createObjectStore('cached_metadata', { keyPath: 'id' });
      }
      
      if (!db.objectStoreNames.contains('cache_metadata')) {
        db.createObjectStore('cache_metadata', { keyPath: 'key' });
      }
    };
  }

  // Calculate current cache size
  async calculateCacheSize() {
    if (!this.initialized) return;
    
    const tx = this.db.transaction(['cached_tracks'], 'readonly');
    const store = tx.objectStore('cached_tracks');
    
    try {
      const allTracks = await this.getAllFromStore(store);
      this.currentCacheSize = allTracks.reduce((sum, track) => {
        return sum + (track.fileSize || 0);
      }, 0);
    } catch (error) {
      console.error('Error calculating cache size:', error);
    }
  }

  // Cache a track for offline access
  async cacheTrack(track, audioBlob) {
    if (!this.initialized) return false;
    
    const fileSize = audioBlob.size;
    const newSize = this.currentCacheSize + fileSize;
    
    // Check if we need to evict tracks
    if (newSize > this.maxCacheSize) {
      await this.evictTracks(newSize - this.maxCacheSize);
    }
    
    const tx = this.db.transaction(['cached_tracks'], 'readwrite');
    const store = tx.objectStore('cached_tracks');
    
    return new Promise((resolve, reject) => {
      const request = store.put({
        id: track.id,
        ...track,
        audioBlob: audioBlob,
        fileSize: fileSize,
        cached_date: new Date(),
        access_count: 0
      });
      
      request.onsuccess = () => {
        this.currentCacheSize += fileSize;
        resolve(true);
      };
      request.onerror = () => reject(false);
    });
  }

  // Get cached track
  async getCachedTrack(trackId) {
    if (!this.initialized) return null;
    
    const tx = this.db.transaction(['cached_tracks'], 'readwrite');
    const store = tx.objectStore('cached_tracks');
    
    return new Promise((resolve, reject) => {
      const request = store.get(trackId);
      request.onsuccess = () => {
        const track = request.result;
        if (track) {
          // Update access count
          track.access_count = (track.access_count || 0) + 1;
          track.last_accessed = new Date();
          store.put(track);
        }
        resolve(track || null);
      };
      request.onerror = () => reject(null);
    });
  }

  // Check if track is cached
  async isTrackCached(trackId) {
    const track = await this.getCachedTrack(trackId);
    return track !== null;
  }

  // Evict least recently used tracks
  async evictTracks(spaceNeeded) {
    const tx = this.db.transaction(['cached_tracks'], 'readwrite');
    const store = tx.objectStore('cached_tracks');
    const accessIndex = store.index('access_count');
    
    const allTracks = await this.getAllFromStore(accessIndex);
    let freed = 0;
    
    // Sort by access count and cache date
    allTracks.sort((a, b) => {
      if (a.access_count !== b.access_count) {
        return a.access_count - b.access_count;
      }
      return new Date(a.cached_date) - new Date(b.cached_date);
    });
    
    for (const track of allTracks) {
      if (freed >= spaceNeeded) break;
      
      const deleteRequest = store.delete(track.id);
      freed += track.fileSize || 0;
      this.currentCacheSize -= track.fileSize || 0;
      
      await new Promise((resolve) => {
        deleteRequest.onsuccess = resolve;
      });
    }
  }

  // Clear all cached content
  async clearCache() {
    if (!this.initialized) return false;
    
    const tx = this.db.transaction(['cached_tracks'], 'readwrite');
    const store = tx.objectStore('cached_tracks');
    
    return new Promise((resolve, reject) => {
      const request = store.clear();
      request.onsuccess = () => {
        this.currentCacheSize = 0;
        resolve(true);
      };
      request.onerror = () => reject(false);
    });
  }

  // Get cache statistics
  async getCacheStats() {
    if (!this.initialized) return {};
    
    const tx = this.db.transaction(['cached_tracks'], 'readonly');
    const store = tx.objectStore('cached_tracks');
    const allTracks = await this.getAllFromStore(store);
    
    return {
      trackCount: allTracks.length,
      cacheSize: this.currentCacheSize,
      maxCacheSize: this.maxCacheSize,
      percentUsed: (this.currentCacheSize / this.maxCacheSize) * 100
    };
  }

  // Get cached tracks list
  async getCachedTracksList() {
    if (!this.initialized) return [];
    
    const tx = this.db.transaction(['cached_tracks'], 'readonly');
    const store = tx.objectStore('cached_tracks');
    const allTracks = await this.getAllFromStore(store);
    
    return allTracks.map(t => ({
      id: t.id,
      title: t.title,
      artist: t.artist,
      duration: t.duration,
      fileSize: t.fileSize,
      cached_date: t.cached_date,
      last_accessed: t.last_accessed,
      access_count: t.access_count
    }));
  }

  // Helper to get all items from store
  getAllFromStore(store) {
    return new Promise((resolve, reject) => {
      const request = store.getAll ? store.getAll() : store.openCursor();
      const results = [];
      
      if (store.getAll) {
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      } else {
        request.onsuccess = (e) => {
          const cursor = e.target.result;
          if (cursor) {
            results.push(cursor.value);
            cursor.continue();
          } else {
            resolve(results);
          }
        };
        request.onerror = () => reject(request.error);
      }
    });
  }

  // Set max cache size
  setMaxCacheSize(sizeInBytes) {
    this.maxCacheSize = sizeInBytes;
  }

  // Get available cache space
  getAvailableCacheSpace() {
    return this.maxCacheSize - this.currentCacheSize;
  }
}

// Global instance
window.offlineCache = null;

// Initialize offline cache
function initOfflineCache() {
  if (window.offlineCache) return;
  window.offlineCache = new OfflineCache();
}

// Export for external use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = OfflineCache;
}
