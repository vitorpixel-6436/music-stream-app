from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.index, name='index'),
    path('player/<uuid:pk>/', views.player, name='player'),
    path('stream/<uuid:pk>/', views.stream_music, name='stream'),
    path('download/<uuid:pk>/', views.download_music, name='download'),
    path('upload/', views.upload_page, name='upload_page'),
    path('api/upload/', views.upload_music, name='upload_music'),
    path('api/search/', views.api_search, name='api_search'),
    
    # Download manager
    path('import/', views.url_import, name='url_import'),
    path('downloads/', views.download_manager, name='download_manager'),
]
