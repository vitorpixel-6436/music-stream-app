"""
Recommendation API Views
========================

REST API endpoints for ML-powered music recommendations.

Endpoints:
- GET  /api/recommendations/          - Personalized recommendations
- GET  /api/track/<id>/similar/       - Similar tracks
- GET  /api/charts/                   - Top charts
- GET  /api/continue-listening/       - Continue listening
- POST /api/track/<id>/play/          - Record play
- GET  /api/listening-stats/          - User stats
"""

import logging
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
import json

from music.models import MusicFile, ListeningHistory
from music.recommendations import RecommendationEngine

logger = logging.getLogger(__name__)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def track_to_dict(track):
    """
    Convert MusicFile to dict for JSON response.
    
    Args:
        track: MusicFile instance
    
    Returns:
        Dict with track data
    """
    return {
        'id': str(track.id),
        'title': track.title,
        'artist': {
            'id': str(track.artist.id),
            'name': track.artist.name,
        },
        'album': {
            'id': str(track.album.id) if track.album else None,
            'title': track.album.title if track.album else None,
        } if track.album else None,
        'genre': {
            'id': str(track.genre.id) if track.genre else None,
            'name': track.genre.name if track.genre else None,
        } if track.genre else None,
        'duration': track.duration,
        'play_count': track.play_count,
        'format': track.format,
        'cover_url': track.cover_image.url if track.cover_image else None,
        'created_at': track.created_at.isoformat(),
    }


# ============================================================================
# API ENDPOINTS
# ============================================================================

@login_required
@require_http_methods(["GET"])
def personalized_recommendations(request):
    """
    Get personalized recommendations for authenticated user.
    
    Query params:
        - limit: Number of recommendations (default 20, max 50)
    
    Returns:
        JSON: {
            'recommendations': [track, ...],
            'count': int,
            'cached': bool
        }
    """
    try:
        limit = min(int(request.GET.get('limit', 20)), 50)
        
        engine = RecommendationEngine()
        recommendations = engine.get_personalized_recommendations(
            user=request.user,
            limit=limit
        )
        
        tracks_data = [track_to_dict(track) for track in recommendations]
        
        return JsonResponse({
            'status': 'success',
            'recommendations': tracks_data,
            'count': len(tracks_data),
            'user': request.user.username,
        })
    
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_http_methods(["GET"])
def similar_tracks(request, track_id):
    """
    Get tracks similar to given track.
    
    Args:
        track_id: UUID of track
    
    Query params:
        - limit: Number of similar tracks (default 10, max 30)
    
    Returns:
        JSON: {
            'similar': [track, ...],
            'count': int,
            'original_track': track
        }
    """
    try:
        track = get_object_or_404(MusicFile, id=track_id)
        limit = min(int(request.GET.get('limit', 10)), 30)
        
        engine = RecommendationEngine()
        similar = engine.get_similar_tracks(
            track=track,
            limit=limit
        )
        
        similar_data = [track_to_dict(t) for t in similar]
        
        return JsonResponse({
            'status': 'success',
            'original_track': track_to_dict(track),
            'similar': similar_data,
            'count': len(similar_data),
        })
    
    except MusicFile.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Track not found'
        }, status=404)
    
    except Exception as e:
        logger.error(f"Similar tracks error: {e}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_http_methods(["GET"])
def top_charts(request):
    """
    Get top trending tracks.
    
    Query params:
        - period: 'weekly' (7 days) or 'monthly' (30 days). Default: weekly
        - limit: Number of tracks (default 20, max 50)
    
    Returns:
        JSON: {
            'charts': [track, ...],
            'count': int,
            'period': str
        }
    """
    try:
        period = request.GET.get('period', 'weekly')
        period_days = 7 if period == 'weekly' else 30
        limit = min(int(request.GET.get('limit', 20)), 50)
        
        engine = RecommendationEngine()
        charts = engine.get_top_charts(
            period_days=period_days,
            limit=limit
        )
        
        charts_data = [track_to_dict(track) for track in charts]
        
        return JsonResponse({
            'status': 'success',
            'charts': charts_data,
            'count': len(charts_data),
            'period': period,
            'period_days': period_days,
        })
    
    except Exception as e:
        logger.error(f"Charts error: {e}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def continue_listening(request):
    """
    Get tracks to continue listening for authenticated user.
    
    Query params:
        - limit: Number of tracks (default 10, max 20)
    
    Returns:
        JSON: {
            'tracks': [track, ...],
            'count': int
        }
    """
    try:
        limit = min(int(request.GET.get('limit', 10)), 20)
        
        engine = RecommendationEngine()
        tracks = engine.get_continue_listening(
            user=request.user,
            limit=limit
        )
        
        tracks_data = [track_to_dict(track) for track in tracks]
        
        return JsonResponse({
            'status': 'success',
            'tracks': tracks_data,
            'count': len(tracks_data),
            'user': request.user.username,
        })
    
    except Exception as e:
        logger.error(f"Continue listening error: {e}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def record_play(request, track_id):
    """
    Record a track play in listening history.
    
    Args:
        track_id: UUID of track
    
    POST data (JSON):
        - duration: How long listened (seconds)
        - position: Position stopped at (seconds)
        - source: Where played from (optional)
        - device: Device type (optional)
    
    Returns:
        JSON: {
            'status': 'success',
            'play_id': UUID
        }
    """
    try:
        track = get_object_or_404(MusicFile, id=track_id)
        
        # Parse JSON body
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            data = {}
        
        # Extract data
        duration = int(data.get('duration', 0))
        position = int(data.get('position', 0))
        source = data.get('source', '')
        device = data.get('device', 'web')
        
        # Record play
        play = ListeningHistory.record_play(
            user=request.user,
            track=track,
            duration=duration,
            position=position,
            source=source,
            device=device
        )
        
        return JsonResponse({
            'status': 'success',
            'play_id': str(play.id),
            'completion_percentage': play.completion_percentage,
            'message': 'Play recorded successfully'
        })
    
    except MusicFile.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Track not found'
        }, status=404)
    
    except Exception as e:
        logger.error(f"Record play error: {e}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def listening_stats(request):
    """
    Get listening statistics for authenticated user.
    
    Query params:
        - days: Number of days to analyze (default 30, max 365)
    
    Returns:
        JSON: {
            'stats': {
                'total_plays': int,
                'unique_tracks': int,
                'total_duration': int (seconds),
                'skip_rate': float,
                'completion_rate': float
            },
            'period_days': int
        }
    """
    try:
        days = min(int(request.GET.get('days', 30)), 365)
        
        stats = ListeningHistory.get_user_stats(
            user=request.user,
            days=days
        )
        
        return JsonResponse({
            'status': 'success',
            'stats': stats,
            'period_days': days,
            'user': request.user.username,
        })
    
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def recent_plays(request):
    """
    Get recent plays for authenticated user.
    
    Query params:
        - limit: Number of plays (default 20, max 100)
    
    Returns:
        JSON: {
            'plays': [
                {
                    'id': UUID,
                    'track': track_dict,
                    'played_at': ISO datetime,
                    'completion': int,
                    'duration': int,
                    'source': str
                },
                ...
            ]
        }
    """
    try:
        limit = min(int(request.GET.get('limit', 20)), 100)
        
        plays = ListeningHistory.objects.filter(
            user=request.user
        ).select_related(
            'track', 'track__artist', 'track__album', 'track__genre'
        ).order_by('-played_at')[:limit]
        
        plays_data = [
            {
                'id': str(play.id),
                'track': track_to_dict(play.track),
                'played_at': play.played_at.isoformat(),
                'completion_percentage': play.completion_percentage,
                'playback_duration': play.playback_duration,
                'source': play.source,
                'device': play.device,
                'skipped': play.skipped,
            }
            for play in plays
        ]
        
        return JsonResponse({
            'status': 'success',
            'plays': plays_data,
            'count': len(plays_data),
            'user': request.user.username,
        })
    
    except Exception as e:
        logger.error(f"Recent plays error: {e}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
