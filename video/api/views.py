import os
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse, Http404

from .serializers import VideoUploadSerializer, VideoListSerializer
from ..models import Video
from .tasks import process_video
from .functions import (
    get_hls_manifest_by_resolution, 
    get_hls_segment_path
)


class VideoUploadView(APIView):
    """
    API endpoint to upload videos.
    Accepts multipart/form-data for video upload.
    Triggers asynchronous processing after saving.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = VideoUploadSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.save()
            process_video.delay(video.id)
            return Response(
                {"detail": "Video hochgeladen. Verarbeitung läuft im Hintergrund."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoListView(APIView):
    """
    API endpoint to list all videos according to API specification.
    Returns: id, created_at, title, description, thumbnail_url, category
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        videos = Video.objects.all().order_by('-upload_date')
        serializer = VideoListSerializer(videos, many=True, context={"request": request})
        return Response(serializer.data)


class HLSManifestView(APIView):
    """
    API endpoint to serve HLS master playlist (index.m3u8) files.
    Returns m3u8 playlist for adaptive streaming.
    """
    permission_classes = [AllowAny]

    def get(self, request, movie_id, resolution):
        try:
            video = Video.objects.get(pk=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video not found")

        manifest = get_hls_manifest_by_resolution(video, resolution)
        if not manifest or not os.path.exists(manifest.path):
            return HttpResponse("Manifest not available.", status=404)

        with open(manifest.path, 'r') as f:
            content = f.read()

        response = HttpResponse(content, content_type='application/vnd.apple.mpegurl')
        response['Cache-Control'] = 'no-cache'
        return response


class HLSSegmentView(APIView):
    """
    API endpoint to serve HLS video segments (.ts files).
    Returns binary video segments for streaming.
    """
    permission_classes = [AllowAny]

    def get(self, request, movie_id, resolution, segment):
        try:
            video = Video.objects.get(pk=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video not found")

        segment_path = get_hls_segment_path(video, resolution, segment)
        if not segment_path:
            return HttpResponse("Segment not found.", status=404)

        with open(segment_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='video/MP2T')
            response['Cache-Control'] = 'max-age=31536000'  # Cache für 1 Jahr
            return response