// Music Player JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Music Streaming App v2.0 initialized');

    const audioPlayers = document.querySelectorAll('audio');
    let currentPlaying = null;

    // --- Keyboard Shortcuts (Global UX) ---
    document.addEventListener('keydown', (e) => {
        // Space to toggle play/pause of the current/last player
        if (e.code === 'Space' && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
            e.preventDefault();
            if (currentPlaying) {
                if (currentPlaying.paused) currentPlaying.play();
                else currentPlaying.pause();
                showNotification(currentPlaying.paused ? 'Paused' : 'Playing');
            }
        }
        // M to mute/unmute
        if (e.key.toLowerCase() === 'm') {
            if (currentPlaying) {
                currentPlaying.muted = !currentPlaying.muted;
                showNotification(currentPlaying.muted ? 'Muted' : 'Unmuted');
            }
        }
    });

    audioPlayers.forEach(player => {
        player.addEventListener('play', function() {
            // Stop other players if one starts (prevent overlapping audio)
            if (currentPlaying && currentPlaying !== this) {
                currentPlaying.pause();
            }
            currentPlaying = this;
            
            // Highlight active track
            const trackItem = this.closest('.track-item');
            if (trackItem) {
                document.querySelectorAll('.track-item').forEach(i => i.classList.remove('active-track'));
                trackItem.classList.add('active-track');
            }
        });

        player.addEventListener('error', function() {
            showNotification('Error loading audio track', 'error');
        });
    });

    // --- Micro-interactions & Click feedback ---
    const trackItems = document.querySelectorAll('.track-item');
    trackItems.forEach(item => {
        item.addEventListener('click', function(e) {
            if (e.target.tagName !== 'BUTTON' && e.target.tagName !== 'A' && e.target.tagName !== 'AUDIO') {
                const player = this.querySelector('audio');
                if (player) {
                    if (player.paused) player.play();
                    else player.pause();
                }
            }
        });
    });

    // --- Toast Notification System ---
    function showNotification(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast-popup ${type}`;
        toast.innerHTML = `<span>${message}</span>`;
        document.body.appendChild(toast);
        
        // Animate in
        setTimeout(() => toast.classList.add('show'), 10);
        
        // Remove after 3s
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
});

// Helper for duration formatting
function formatDuration(seconds) {
    const min = Math.floor(seconds / 60);
    const sec = Math.floor(seconds % 60);
    return `${min}:${sec.toString().padStart(2, '0')}`;
}
