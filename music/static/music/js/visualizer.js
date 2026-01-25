/**
 * Audio Visualizer Module
 * Provides real-time visualization of audio frequencies using Canvas API
 * Animated spectrum bars synchronized with audio playback
 */

class AudioVisualizer {
    constructor(canvasElement, audioContext, analyser) {
        this.canvas = canvasElement;
        this.ctx = this.canvas.getContext('2d');
        this.audioContext = audioContext;
        this.analyser = analyser;
        
        // Canvas sizing
        this.canvas.width = this.canvas.offsetWidth;
        this.canvas.height = this.canvas.offsetHeight;
        
        // Frequency data
        this.dataArray = new Uint8Array(this.analyser.frequencyBinCount);
        this.bars = 64;
        this.barWidth = this.canvas.width / this.bars;
        
        // Animation
        this.animationId = null;
        this.isRunning = false;
        
        // Color scheme
        this.colors = {
            background: '#0f0f1e',
            gradient: ['#ff00ff', '#00ffff', '#00ff00', '#ffff00', '#ff6600']
        };
        
        this.init();
    }
    
    init() {
        // Draw initial background
        this.clear();
        
        // Handle window resize
        window.addEventListener('resize', () => this.handleResize());
    }
    
    handleResize() {
        this.canvas.width = this.canvas.offsetWidth;
        this.canvas.height = this.canvas.offsetHeight;
        this.barWidth = this.canvas.width / this.bars;
    }
    
    clear() {
        this.ctx.fillStyle = this.colors.background;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }
    
    start() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.animate();
    }
    
    stop() {
        this.isRunning = false;
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        this.clear();
    }
    
    animate() {
        this.animationId = requestAnimationFrame(() => this.animate());
        
        // Get frequency data
        this.analyser.getByteFrequencyData(this.dataArray);
        
        // Clear canvas with slight transparency for trail effect
        this.ctx.fillStyle = 'rgba(15, 15, 30, 0.1)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw bars
        this.drawBars();
    }
    
    drawBars() {
        const barCount = Math.min(this.bars, this.dataArray.length);
        
        for (let i = 0; i < barCount; i++) {
            const value = this.dataArray[i];
            const percent = value / 255;
            const height = percent * this.canvas.height;
            const x = i * this.barWidth;
            const y = this.canvas.height - height;
            
            // Create gradient color
            const hue = (i / barCount) * 360;
            this.ctx.fillStyle = `hsl(${hue}, 100%, 50%)`;
            
            // Draw bar with glow effect
            this.ctx.shadowColor = `hsl(${hue}, 100%, 50%)`;
            this.ctx.shadowBlur = 10;
            this.ctx.fillRect(x, y, this.barWidth - 2, height);
        }
        
        // Reset shadow
        this.ctx.shadowColor = 'transparent';
        this.ctx.shadowBlur = 0;
    }
    
    drawWaveform() {
        const bufferLength = this.analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        this.analyser.getByteTimeDomainData(dataArray);
        
        this.clear();
        
        this.ctx.lineWidth = 2;
        this.ctx.strokeStyle = '#00ff00';
        this.ctx.beginPath();
        
        const sliceWidth = this.canvas.width / bufferLength;
        let x = 0;
        
        for (let i = 0; i < bufferLength; i++) {
            const v = dataArray[i] / 128.0;
            const y = v * this.canvas.height / 2;
            
            if (i === 0) {
                this.ctx.moveTo(x, y);
            } else {
                this.ctx.lineTo(x, y);
            }
            
            x += sliceWidth;
        }
        
        this.ctx.lineTo(this.canvas.width, this.canvas.height / 2);
        this.ctx.stroke();
    }
    
    getVisualizationType() {
        return localStorage.getItem('visualizer_type') || 'bars';
    }
    
    setVisualizationType(type) {
        localStorage.setItem('visualizer_type', type);
    }
}

// Global instance
window.visualizer = null;

// Initialize visualizer when needed
function initVisualizer(canvasSelector = '#visualizer-canvas') {
    if (window.visualizer) return;
    
    const canvas = document.querySelector(canvasSelector);
    const audioContext = window.audioContext;
    const analyser = window.equalizer ? window.equalizer.analyser : null;
    
    if (canvas && audioContext && analyser) {
        window.visualizer = new AudioVisualizer(canvas, audioContext, analyser);
    }
}

// Export for external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AudioVisualizer;
}
