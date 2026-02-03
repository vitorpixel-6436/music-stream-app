from django.urls import path
from . import views
from . import download_views
from . import recommendation_views

app_name = 'music'

urlpatterns = [
    # ============================================================================
    # Main Pages
    # ============================================================================
    path('', views.index, name='index'),
    path('player/<uuid:pk>/', views.player, name='player'),
    
    # ============================================================================
    # Music Streaming & Downloads
    # ============================================================================
    path('stream/<uuid:pk>/', views.stream_music, name='stream'),
    path('download/<uuid:pk>/', views.download_music, name='download'),
    
    # ============================================================================
    # Upload Management
    # ============================================================================
    path('upload/', views.upload_page, name='upload_page'),
    path('api/upload/', views.upload_music, name='upload_music'),
    
    # ============================================================================
    # Search & Discovery
    # ============================================================================
    path('api/search/', views.api_search, name='api_search'),
    
    # ============================================================================
    # ML Recommendations API (v1.3.0)
    # ============================================================================
    
    # Personalized recommendations
    path('api/recommendations/', 
         recommendation_views.personalized_recommendations, 
         name='api_recommendations'),
    
    # Similar tracks
    path('api/track/<uuid:track_id>/similar/', 
         recommendation_views.similar_tracks, 
         name='api_similar_tracks'),
    
    # Top charts
    path('api/charts/', 
         recommendation_views.top_charts, 
         name='api_charts'),
    
    # Continue listening
    path('api/continue-listening/', 
         recommendation_views.continue_listening, 
         name='api_continue_listening'),
    
    # Record play
    path('api/track/<uuid:track_id>/play/', 
         recommendation_views.record_play, 
         name='api_record_play'),
    
    # User stats
    path('api/listening-stats/', 
         recommendation_views.listening_stats, 
         name='api_listening_stats'),
    
    # Recent plays
    path('api/recent-plays/', 
         recommendation_views.recent_plays, 
         name='api_recent_plays'),
    
    # ============================================================================
    # Download Manager (URL Import)
    # ============================================================================
    
    # Main pages
    path('downloads/', download_views.download_list, name='download_manager'),
    path('downloads/create/', download_views.download_create, name='download_create'),
    
    # Task management
    path('downloads/<uuid:task_id>/cancel/', download_views.download_cancel, name='download_cancel'),
    path('downloads/<uuid:task_id>/retry/', download_views.download_retry, name='download_retry'),
    
    # API endpoints for AJAX
    path('api/downloads/<uuid:task_id>/status/', download_views.download_status_api, name='download_status_api'),
    path('api/downloads/bulk-status/', download_views.download_bulk_status, name='download_bulk_status'),
    
    # Legacy compatibility (redirect to new endpoints)
    path('import/', download_views.download_create, name='url_import'),
]
