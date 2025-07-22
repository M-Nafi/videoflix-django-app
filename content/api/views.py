import os
import logging
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.renderers import BaseRenderer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.http import Http404, FileResponse
from django.conf import settings

from .serializers import VideoUploadSerializer, VideoListSerializer
from ..models import Video

logger = logging.getLogger(__name__)

class M3U8Renderer(BaseRenderer):
    """Custom renderer for HLS manifest files."""
    media_type = 'application/vnd.apple.mpegurl'
    format = 'm3u8'
    charset = None
    render_style = 'binary'
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class TSRenderer(BaseRenderer):
    """Custom renderer for HLS segments."""
    media_type = 'video/MP2T'
    format = 'ts'
    charset = None
    render_style = 'binary'
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

class VideoUploadView(APIView):
    """
    API endpoint to upload videos.
    Accepts multipart/form-data for video upload.
    Triggers asynchronous processing after saving.
    """
    permission_classes = [IsAdminUser]
    authentication_classes = []
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = VideoUploadSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.save()
            return Response(
                {"detail": "Video hochgeladen. Verarbeitung läuft im Hintergrund."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VideoListView(APIView):
    """
    API endpoint to list all videos according to API specification.
    Returns: id, created_at, title, description, thumbnail_url, category
    
    FIXED: Robustes Error Handling, besseres Logging
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            videos = Video.objects.all().order_by('-upload_date')
            serializer = VideoListSerializer(videos, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error in VideoListView: {e}", exc_info=True)
            return Response(
                {"error": "Unable to fetch videos", "detail": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class HLSManifestView(APIView):
    """
    API endpoint to serve HLS master playlist (index.m3u8) files.
    FIXED: Basiert auf funktionierender Referenz-Implementation
    """
    renderer_classes = [M3U8Renderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, movie_id, resolution):
        try:
            video = Video.objects.get(pk=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video nicht gefunden.")
        
        media_root = settings.MEDIA_ROOT
        basename, _ = os.path.splitext(os.path.basename(video.original_file.name))
        hls_dir = os.path.join(media_root, f'videos/hls/{resolution}/{basename}')
        manifest_path = os.path.join(hls_dir, "index.m3u8")
        
        if not os.path.isfile(manifest_path):
            raise Http404("HLS-Manifest nicht gefunden.")
        
        return FileResponse(open(manifest_path, "rb"), content_type="application/vnd.apple.mpegurl")


class HLSSegmentView(APIView):
    """
    API endpoint to serve HLS video segments (.ts files).
    FIXED: Basiert auf funktionierender Referenz-Implementation
    """
    renderer_classes = [TSRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, movie_id, resolution, segment):
        try:
            video = Video.objects.get(pk=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video nicht gefunden.")
        
        media_root = settings.MEDIA_ROOT
        basename, _ = os.path.splitext(os.path.basename(video.original_file.name))
        hls_dir = os.path.join(media_root, f'videos/hls/{resolution}/{basename}')
        segment_path = os.path.join(hls_dir, segment)
        
        if not os.path.isfile(segment_path):
            raise Http404("HLS-Segment nicht gefunden.")
        
        return FileResponse(open(segment_path, "rb"), content_type="video/MP2T")
