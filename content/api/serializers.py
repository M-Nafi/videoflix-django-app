import logging
from rest_framework import serializers
from ..models import Video

logger = logging.getLogger(__name__)


class VideoUploadSerializer(serializers.ModelSerializer):
    """Serializer for uploading new video entries."""
    
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'original_file', 'genre']


class VideoListSerializer(serializers.ModelSerializer):
    """Serializer for listing videos according to API specification."""
    
    created_at = serializers.DateTimeField(source='upload_date', read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    category = serializers.CharField(read_only=True)

    class Meta:
        model = Video
        fields = ['id', 'created_at', 'title', 'description', 'thumbnail_url', 'category']

    def get_thumbnail_url(self, obj):
        """Return the absolute URL of the thumbnail image."""
        request = self.context.get('request')
        
        if obj.thumbnail:
            try:
                if hasattr(obj.thumbnail, 'url'):
                    thumbnail_url = obj.thumbnail.url
                    if request:
                        return request.build_absolute_uri(thumbnail_url)
                    return thumbnail_url
            except (ValueError, OSError, AttributeError):
                logger.debug(f"Thumbnail file missing for video {obj.id}")
                return None
        
        return None
