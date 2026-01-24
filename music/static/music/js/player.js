// Music Player JavaScript

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Music Streaming App initialized');
    
    // Get all audio players on the page
    const audioPlayers = document.querySelectorAll('audio');
    
    audioPlayers.forEach(player => {
        // Add event listener for when audio starts playing
        player.addEventListener('play', function() {
            console.log('Playing:', this.src);
        });
        
        // Add event listener for when audio is paused
        player.addEventListener('pause', function() {
            console.log('Paused:', this.src);
        });
        
        // Add event listener for when audio ends
        player.addEventListener('ended', function() {
            console.log('Finished playing:', this.src);
        });
        
        // Add event listener for errors
        player.addEventListener('error', function() {
            console.error('Error loading audio:', this.src);
        });
    });
    
    // Handle track item clicks for smooth scrolling
    const trackItems = document.querySelectorAll('.track-item');
    trackItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 8px rgba(0,0,0,0.15)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
        });
    });
});

// Helper function to format time duration
function formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

// Helper function to update player progress
function updateProgress(player) {
    if (player.duration) {
        const progress = (player.currentTime / player.duration) * 100;
        return progress;
    }
    return 0;
}
