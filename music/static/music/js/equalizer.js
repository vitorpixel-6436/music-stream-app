/**
 * Audio Equalizer Module
 * Provides browser-based audio equalization using Web Audio API
 * Features: 5-band EQ, presets, and real-time audio processing
 */

class AudioEqualizer {
    constructor(audioElement) {
        this.audioElement = audioElement;
        this.audioContext = null;
        this.analyser = null;
        this.gainNodes = [];
        this.initialized = false;
        
        // EQ Bands: [60Hz, 250Hz, 1kHz, 4kHz, 16kHz]
        this.frequencies = [60, 250, 1000, 4000, 16000];
        this.gains = [0, 0, 0, 0, 0];
        
        // Presets
        this.presets = {
            flat: [0, 0, 0, 0, 0],
            bass: [6, 3, 0, -2, -4],
            treble: [-4, -2, 0, 3, 6],
            vocal: [2, 4, 3, 1, -1],
            warm: [4, 2, 0, -1, -3],
            bright: [-2, 0, 2, 4, 3]
        };
        
        this.init();
    }
    
    init() {
        try {
            const audioContext = this.getAudioContext();
            if (!audioContext) return;
            
            this.audioContext = audioContext;
            
            // Create audio source from HTML audio element
            const source = this.audioContext.createMediaElementAudioSource(this.audioElement);
            
            // Create analyser for visualization
            this.analyser = this.audioContext.createAnalyser();
            this.analyser.fftSize = 256;
            
            // Create gain nodes for each frequency band
            const filterGains = [];
            let previousNode = source;
            
            this.frequencies.forEach((freq) => {
                const filter = this.audioContext.createBiquadFilter();
                filter.type = 'peaking';
                filter.frequency.value = freq;
                filter.Q.value = 1;
                filter.gain.value = 0;
                
                previousNode.connect(filter);
                filterGains.push(filter);
                previousNode = filter;
            });
            
            this.gainNodes = filterGains;
            previousNode.connect(this.analyser);
            this.analyser.connect(this.audioContext.destination);
            
            this.initialized = true;
        } catch (e) {
            console.warn('AudioEqualizer: Web Audio API not available or blocked', e);
        }
    }
    
    getAudioContext() {
        if (window.audioContext) return window.audioContext;
        
        try {
            const context = new (window.AudioContext || window.webkitAudioContext)();
            window.audioContext = context;
            return context;
        } catch (e) {
            console.warn('Web Audio API not supported');
            return null;
        }
    }
    
    setGain(bandIndex, gain) {
        if (bandIndex < 0 || bandIndex >= this.gainNodes.length) return;
        
        const clampedGain = Math.max(-12, Math.min(12, gain));
        this.gains[bandIndex] = clampedGain;
        this.gainNodes[bandIndex].gain.value = clampedGain;
    }
    
    applyPreset(presetName) {
        if (!this.presets[presetName]) return;
        
        const preset = this.presets[presetName];
        preset.forEach((gain, index) => {
            this.setGain(index, gain);
        });
    }
    
    getFrequencyData() {
        if (!this.analyser) return null;
        
        const dataArray = new Uint8Array(this.analyser.frequencyBinCount);
        this.analyser.getByteFrequencyData(dataArray);
        return dataArray;
    }
    
    reset() {
        this.gains.forEach((_, index) => {
            this.setGain(index, 0);
        });
    }
    
    getGains() {
        return [...this.gains];
    }
    
    saveSettings() {
        localStorage.setItem('eq_presets', JSON.stringify({
            gains: this.gains,
            timestamp: Date.now()
        }));
    }
    
    loadSettings() {
        const saved = localStorage.getItem('eq_presets');
        if (saved) {
            const settings = JSON.parse(saved);
            settings.gains.forEach((gain, index) => {
                this.setGain(index, gain);
            });
        }
    }
}

// Global instance
window.equalizer = null;

// Initialize equalizer when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const audioElement = document.querySelector('audio');
    if (audioElement && !window.equalizer) {
        window.equalizer = new AudioEqualizer(audioElement);
        window.equalizer.loadSettings();
    }
});
