from django.urls import path
from . import views
from . import download_views

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
