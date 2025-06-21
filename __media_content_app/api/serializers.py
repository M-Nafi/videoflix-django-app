from rest_framework import serializers
from __media_content_app.models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_file', 'thumbnail', 'uploaded_at']


