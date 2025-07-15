from rest_framework import serializers
from ..models import Video


class VideoUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for uploading new video entries.

    Includes fields for ID, title, description, original file, and genre.
    """
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'original_file', 'genre']


class VideoListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing videos according to API specification.

    Provides fields: id, created_at, title, description, thumbnail_url, category.
    Maps upload_date to created_at and genre to category for API compatibility.
    """
    created_at = serializers.DateTimeField(source='upload_date', read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    category = serializers.CharField(source='category', read_only=True)

    class Meta:
        model = Video
        fields = ['id', 'created_at', 'title', 'description', 'thumbnail_url', 'category']

    def get_thumbnail_url(self, obj):
        """
        Return the absolute URL of the thumbnail image.
        
        Args:
            obj: Video instance.
            
        Returns:
            str or None: Absolute URL of the thumbnail or None if unavailable.
        """
        request = self.context.get('request')
        if obj.thumbnail and hasattr(obj.thumbnail, 'url'):
            return request.build_absolute_uri(obj.thumbnail.url) if request else obj.thumbnail.url
        return None