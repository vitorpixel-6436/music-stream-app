/**
 * WebSocket Manager for Real-Time Features
 * Handles connections to Django Channels WebSocket consumers
 */

class WebSocketManager {
    constructor() {
        this.sockets = {};
        this.reconnectIntervals = {};
        this.maxReconnectAttempts = 5;
    }

    /**
     * Create a WebSocket connection
     * @param {string} name - Unique name for this socket
     * @param {string} url - WebSocket URL
     * @param {object} callbacks - Event callbacks (onMessage, onOpen, onClose, onError)
     */
    connect(name, url, callbacks = {}) {
        if (this.sockets[name]) {
            console.warn(`WebSocket '${name}' already exists`);
            return this.sockets[name];
        }

        const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        const fullUrl = `${wsProtocol}${window.location.host}${url}`;

        const socket = new WebSocket(fullUrl);
        this.sockets[name] = socket;

        socket.onopen = (event) => {
            console.log(`WebSocket '${name}' connected`);
            this.reconnectIntervals[name] = 0;
            if (callbacks.onOpen) callbacks.onOpen(event);
        };

        socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (callbacks.onMessage) callbacks.onMessage(data);
            } catch (error) {
                console.error('Error parsing WebSocket message:', error);
            }
        };

        socket.onerror = (error) => {
            console.error(`WebSocket '${name}' error:`, error);
            if (callbacks.onError) callbacks.onError(error);
        };

        socket.onclose = (event) => {
            console.log(`WebSocket '${name}' closed`);
            delete this.sockets[name];

            if (callbacks.onClose) callbacks.onClose(event);

            // Auto-reconnect logic
            if (!this.reconnectIntervals[name]) {
                this.reconnectIntervals[name] = 0;
            }

            if (this.reconnectIntervals[name] < this.maxReconnectAttempts) {
                const delay = Math.min(1000 * Math.pow(2, this.reconnectIntervals[name]), 30000);
                console.log(`Reconnecting '${name}' in ${delay}ms...`);
                setTimeout(() => {
                    this.reconnectIntervals[name]++;
                    this.connect(name, url, callbacks);
                }, delay);
            }
        };

        return socket;
    }

    /**
     * Send message through a WebSocket
     * @param {string} name - Socket name
     * @param {object} data - Data to send
     */
    send(name, data) {
        const socket = this.sockets[name];
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify(data));
        } else {
            console.warn(`WebSocket '${name}' is not open`);
        }
    }

    /**
     * Close a WebSocket connection
     * @param {string} name - Socket name
     */
    disconnect(name) {
        const socket = this.sockets[name];
        if (socket) {
            this.reconnectIntervals[name] = this.maxReconnectAttempts; // Prevent reconnect
            socket.close();
            delete this.sockets[name];
        }
    }

    /**
     * Disconnect all WebSocket connections
     */
    disconnectAll() {
        Object.keys(this.sockets).forEach(name => this.disconnect(name));
    }
}

// Export singleton instance
const wsManager = new WebSocketManager();


/**
 * Track Listeners WebSocket
 * Shows real-time count of listeners for a specific track
 */
class TrackListenersSocket {
    constructor(trackId, onUpdate) {
        this.trackId = trackId;
        this.onUpdate = onUpdate;
        this.socketName = `track_listeners_${trackId}`;

        wsManager.connect(this.socketName, `/ws/track/${trackId}/listeners/`, {
            onMessage: (data) => {
                if (data.type === 'listener_count') {
                    this.onUpdate(data.count);
                }
            },
            onOpen: () => {
                console.log(`Listening to track ${trackId} listener updates`);
            }
        });
    }

    disconnect() {
        wsManager.disconnect(this.socketName);
    }
}


/**
 * Now Playing WebSocket
 * Shows what tracks are being played globally in real-time
 */
class NowPlayingSocket {
    constructor(onTrackPlaying) {
        this.onTrackPlaying = onTrackPlaying;
        this.socketName = 'now_playing';

        wsManager.connect(this.socketName, '/ws/now-playing/', {
            onMessage: (data) => {
                if (data.type === 'track_playing') {
                    this.onTrackPlaying(data);
                }
            }
        });
    }

    /**
     * Broadcast that user started playing a track
     * @param {object} trackData - Track information
     */
    broadcastTrackStart(trackData) {
        wsManager.send(this.socketName, {
            type: 'track_start',
            ...trackData
        });
    }

    disconnect() {
        wsManager.disconnect(this.socketName);
    }
}


// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { wsManager, TrackListenersSocket, NowPlayingSocket };
}
