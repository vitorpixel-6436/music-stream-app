import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.cache import cache


class TrackListenersConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time track listener count updates.
    Broadcasts how many users are currently listening to each track.
    """

    async def connect(self):
        self.track_id = self.scope['url_route']['kwargs'].get('track_id')
        self.room_group_name = f'track_{self.track_id}_listeners'

        # Join track listeners group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Increment listener count
        await self.increment_listeners()

        # Send current listener count
        count = await self.get_listener_count()
        await self.send(text_data=json.dumps({
            'type': 'listener_count',
            'track_id': self.track_id,
            'count': count
        }))

    async def disconnect(self, close_code):
        # Decrement listener count
        await self.decrement_listeners()

        # Send updated count to group
        count = await self.get_listener_count()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'listener_count_message',
                'track_id': self.track_id,
                'count': count
            }
        )

        # Leave track listeners group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'ping':
            # Heartbeat to keep connection alive
            await self.send(text_data=json.dumps({
                'type': 'pong'
            }))

    async def listener_count_message(self, event):
        """Send listener count update to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'listener_count',
            'track_id': event['track_id'],
            'count': event['count']
        }))

    @database_sync_to_async
    def increment_listeners(self):
        """Increment the listener count for a track in cache"""
        cache_key = f'track_listeners_{self.track_id}'
        current_count = cache.get(cache_key, 0)
        cache.set(cache_key, current_count + 1, timeout=None)
        return current_count + 1

    @database_sync_to_async
    def decrement_listeners(self):
        """Decrement the listener count for a track in cache"""
        cache_key = f'track_listeners_{self.track_id}'
        current_count = cache.get(cache_key, 0)
        new_count = max(0, current_count - 1)
        cache.set(cache_key, new_count, timeout=None)
        return new_count

    @database_sync_to_async
    def get_listener_count(self):
        """Get current listener count for a track"""
        cache_key = f'track_listeners_{self.track_id}'
        return cache.get(cache_key, 0)


class NowPlayingConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for broadcasting now playing updates across all users.
    Shows what tracks are being played in real-time globally.
    """

    async def connect(self):
        self.room_group_name = 'now_playing'

        # Join now playing group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave now playing group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'track_start':
            # Broadcast track start to all connected clients
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'track_playing',
                    'track_id': data.get('track_id'),
                    'track_title': data.get('track_title'),
                    'artist': data.get('artist'),
                    'user_id': data.get('user_id')
                }
            )

    async def track_playing(self, event):
        """Send track playing update to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'track_playing',
            'track_id': event['track_id'],
            'track_title': event['track_title'],
            'artist': event['artist'],
            'user_id': event.get('user_id')
        }))
