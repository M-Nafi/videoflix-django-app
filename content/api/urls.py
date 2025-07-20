from django.urls import path

from .views import (
    VideoUploadView, 
    VideoListView, 
    HLSManifestView,
    HLSSegmentView
)

urlpatterns = [
    # Upload endpoint - für Admin-Upload
    path('upload/', VideoUploadView.as_view(), name='video-upload'),
    
    # API-konforme Endpoints laut Spezifikation
    path('video/', VideoListView.as_view(), name='video-list'),
    
    # HLS Streaming Endpoints
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', 
         HLSManifestView.as_view(), name='hls-manifest'),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>/', 
         HLSSegmentView.as_view(), name='hls-segment'),
]