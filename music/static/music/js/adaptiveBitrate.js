/**
 * Adaptive Bitrate Streaming Module
 * Automatically adjusts audio quality based on network conditions
 * Features: Network detection, quality switching, buffering management
 */

class AdaptiveBitrate {
  constructor() {
    this.bitrates = [
      { label: 'Low (64kbps)', bitrate: 64000 },
      { label: 'Medium (128kbps)', bitrate: 128000 },
      { label: 'High (192kbps)', bitrate: 192000 },
      { label: 'Very High (320kbps)', bitrate: 320000 }
    ];
    this.currentBitrate = this.bitrates[1]; // Default to 128kbps
    this.networkSpeed = 0;
    this.bufferLevel = 0;
    this.isAutomatic = true;
    this.init();
  }

  init() {
    // Monitor network speed and buffer status
    this.monitorNetworkSpeed();
    this.monitorBuffer();
  }

  monitorNetworkSpeed() {
    // Use navigator.connection API if available
    if (navigator.connection) {
      navigator.connection.addEventListener('change', () => {
        this.updateBitrateBasedOnConnection();
      });
      this.updateBitrateBasedOnConnection();
    }
  }

  updateBitrateBasedOnConnection() {
    const connection = navigator.connection;
    if (!connection) return;

    const effectiveType = connection.effectiveType; // 4g, 3g, 2g, slow-2g

    switch (effectiveType) {
      case '4g':
        this.selectBitrate(320000); // Very High
        break;
      case '3g':
        this.selectBitrate(192000); // High
        break;
      case '2g':
        this.selectBitrate(128000); // Medium
        break;
      case 'slow-2g':
        this.selectBitrate(64000); // Low
        break;
    }
  }

  monitorBuffer() {
    // Monitor buffer level and adjust quality
    setInterval(() => {
      const player = document.querySelector('audio');
      if (!player) return;

      // Calculate buffer percentage
      if (player.buffered.length > 0) {
        this.bufferLevel = (player.buffered.end(player.buffered.length - 1) / player.duration) * 100;
        
        if (this.isAutomatic) {
          this.adjustQualityBasedOnBuffer();
        }
      }
    }, 1000);
  }

  adjustQualityBasedOnBuffer() {
    // If buffer is low, reduce quality
    if (this.bufferLevel < 20) {
      const lowerBitrate = this.getLowerBitrate();
      if (lowerBitrate) {
        this.selectBitrate(lowerBitrate.bitrate);
        console.log('Buffer low, reducing quality to', lowerBitrate.label);
      }
    }
    // If buffer is high, increase quality
    else if (this.bufferLevel > 80) {
      const higherBitrate = this.getHigherBitrate();
      if (higherBitrate) {
        this.selectBitrate(higherBitrate.bitrate);
        console.log('Buffer high, increasing quality to', higherBitrate.label);
      }
    }
  }

  selectBitrate(bitrate) {
    const found = this.bitrates.find(b => b.bitrate === bitrate);
    if (found && found.bitrate !== this.currentBitrate.bitrate) {
      this.currentBitrate = found;
      this.notifyBitrateChange();
    }
  }

  getLowerBitrate() {
    const currentIndex = this.bitrates.findIndex(b => b.bitrate === this.currentBitrate.bitrate);
    return currentIndex > 0 ? this.bitrates[currentIndex - 1] : null;
  }

  getHigherBitrate() {
    const currentIndex = this.bitrates.findIndex(b => b.bitrate === this.currentBitrate.bitrate);
    return currentIndex < this.bitrates.length - 1 ? this.bitrates[currentIndex + 1] : null;
  }

  notifyBitrateChange() {
    const event = new CustomEvent('bitrateChanged', {
      detail: {
        bitrate: this.currentBitrate.bitrate,
        label: this.currentBitrate.label
      }
    });
    document.dispatchEvent(event);
  }

  setAutomatic(value) {
    this.isAutomatic = value;
  }

  getCurrentBitrate() {
    return this.currentBitrate;
  }

  getAvailableBitrates() {
    return this.bitrates;
  }

  setBitrate(bitrate) {
    this.isAutomatic = false;
    this.selectBitrate(bitrate);
  }

  getBufferLevel() {
    return this.bufferLevel;
  }

  getNetworkType() {
    if (navigator.connection) {
      return navigator.connection.effectiveType;
    }
    return 'unknown';
  }

  generateStreamUrl(trackId) {
    // Generate streaming URL with bitrate parameter
    return `/api/stream/${trackId}?bitrate=${this.currentBitrate.bitrate}`;
  }
}

// Global instance
window.adaptiveBitrate = null;

// Initialize adaptive bitrate
function initAdaptiveBitrate() {
  if (window.adaptiveBitrate) return;
  window.adaptiveBitrate = new AdaptiveBitrate();
}

// Export for external use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AdaptiveBitrate;
}
