from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.index, name='index'),
    path('player/<int:pk>/', views.player, name='player'),
    path('stream/<int:pk>/', views.stream_music, name='stream'),
    path('download/<int:pk>/', views.download_music, name='download'),
    path('upload/', views.upload_page, name='upload_page'),
    path('api/upload/', views.upload_music, name='upload_music'),
]
