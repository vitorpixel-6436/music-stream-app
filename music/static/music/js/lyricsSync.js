/**
 * Lyrics Sync Module
 * Displays synchronized lyrics with audio playback
 * Features: Line-by-line sync, scroll highlight, timing adjustments
 */

class LyricsSync {
  constructor() {
    this.currentTrack = null;
    this.lyrics = null;
    this.container = null;
    this.isPlaying = false;
    this.currentTime = 0;
    this.lineElements = [];
    this.init();
  }

  init() {
    // Set up event listeners
    document.addEventListener('trackChanged', (e) => this.loadLyrics(e.detail.track));
    document.addEventListener('playbackTime', (e) => this.updateDisplay(e.detail.currentTime));
  }

  // Load lyrics from metadata or API
  async loadLyrics(track) {
    this.currentTrack = track;
    
    try {
      // Try to get lyrics from track metadata first
      if (track.lyrics && track.lyrics.length > 0) {
        this.lyrics = this.parseLyrics(track.lyrics);
      } else {
        // Fallback: fetch from lyrics API
        this.lyrics = await this.fetchLyricsFromAPI(track.title, track.artist);
      }
      
      if (this.lyrics) {
        this.renderLyrics();
      }
    } catch (error) {
      console.error('Error loading lyrics:', error);
    }
  }

  // Parse lyrics with timestamps [mm:ss] or [mm:ss.xx]
  parseLyrics(lyricsText) {
    if (!lyricsText) return null;
    
    const lines = lyricsText.split('\n');
    const parsed = [];
    
    lines.forEach(line => {
      const timeMatch = line.match(/\[(\d{2}):(\d{2})(?:\.(\d{2}))?\](.*)/);
      if (timeMatch) {
        const minutes = parseInt(timeMatch[1]);
        const seconds = parseInt(timeMatch[2]);
        const centiseconds = timeMatch[3] ? parseInt(timeMatch[3]) : 0;
        const time = minutes * 60 + seconds + (centiseconds / 100);
        const text = timeMatch[4].trim();
        
        if (text) {
          parsed.push({ time, text });
        }
      }
    });
    
    return parsed.length > 0 ? parsed : null;
  }

  // Fetch lyrics from external API
  async fetchLyricsFromAPI(title, artist) {
    try {
      const response = await fetch(`/api/lyrics?title=${encodeURIComponent(title)}&artist=${encodeURIComponent(artist)}`);
      if (!response.ok) return null;
      
      const data = await response.json();
      return this.parseLyrics(data.lyrics);
    } catch (error) {
      console.error('Error fetching lyrics from API:', error);
      return null;
    }
  }

  // Render lyrics in container
  renderLyrics() {
    if (!this.lyrics) {
      this.showNoLyrics();
      return;
    }
    
    this.container = document.getElementById('lyrics-container');
    if (!this.container) {
      console.warn('Lyrics container not found');
      return;
    }
    
    this.container.innerHTML = '';
    this.lineElements = [];
    
    this.lyrics.forEach((line, index) => {
      const lineElement = document.createElement('div');
      lineElement.className = 'lyrics-line';
      lineElement.dataset.index = index;
      lineElement.dataset.time = line.time;
      lineElement.textContent = line.text;
      lineElement.style.cursor = 'pointer';
      
      // Click to jump to time
      lineElement.addEventListener('click', () => this.jumpToTime(line.time));
      
      this.container.appendChild(lineElement);
      this.lineElements.push(lineElement);
    });
  }

  // Update lyrics display based on current playback time
  updateDisplay(currentTime) {
    this.currentTime = currentTime;
    
    // Find current and next line
    let currentLineIndex = -1;
    for (let i = this.lyrics.length - 1; i >= 0; i--) {
      if (this.lyrics[i].time <= currentTime) {
        currentLineIndex = i;
        break;
      }
    }
    
    // Update styling
    this.lineElements.forEach((element, index) => {
      element.classList.remove('active', 'next');
      
      if (index === currentLineIndex) {
        element.classList.add('active');
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
      } else if (index === currentLineIndex + 1) {
        element.classList.add('next');
      }
    });
  }

  // Jump to specific time
  jumpToTime(time) {
    const event = new CustomEvent('seekTo', { detail: { time } });
    document.dispatchEvent(event);
  }

  // Adjust timing offset (useful for syncing)
  adjustTiming(offsetMs) {
    if (this.lyrics) {
      const offset = offsetMs / 1000;
      this.lyrics.forEach(line => {
        line.time += offset;
        if (line.time < 0) line.time = 0;
      });
    }
  }

  // Show when no lyrics available
  showNoLyrics() {
    this.container = document.getElementById('lyrics-container');
    if (this.container) {
      this.container.innerHTML = '<div class="lyrics-placeholder">No lyrics available for this track</div>';
    }
  }

  // Toggle lyrics visibility
  toggle() {
    const container = document.getElementById('lyrics-container');
    if (container) {
      container.style.display = container.style.display === 'none' ? 'block' : 'none';
    }
  }

  // Export lyrics as file
  exportLyrics() {
    if (!this.lyrics) return;
    
    let lyricsText = '';
    this.lyrics.forEach(line => {
      const minutes = Math.floor(line.time / 60);
      const seconds = Math.floor(line.time % 60);
      const centiseconds = Math.round((line.time % 1) * 100);
      lyricsText += `[${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}.${String(centiseconds).padStart(2, '0')}]${line.text}\n`;
    });
    
    const blob = new Blob([lyricsText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${this.currentTrack.title}.lrc`;
    a.click();
    URL.revokeObjectURL(url);
  }
}

// Global instance
window.lyricsSync = null;

// Initialize lyrics sync
function initLyricsSync() {
  if (window.lyricsSync) return;
  window.lyricsSync = new LyricsSync();
}

// Export for external use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = LyricsSync;
}
