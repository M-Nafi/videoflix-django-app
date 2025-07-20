from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    original_file = models.FileField(
        upload_to='videos/original/', max_length=255)
    thumbnail = models.ImageField(
        upload_to='videos/thumbnails/', max_length=255, null=True, blank=True)

    # Standard video files  
    video_180p = models.FileField(
        upload_to='videos/180p/', null=True, blank=True, max_length=255)
    video_360p = models.FileField(
        upload_to='videos/360p/', null=True, blank=True, max_length=255)
    video_720p = models.FileField(
        upload_to='videos/720p/', null=True, blank=True, max_length=255)
    video_1080p = models.FileField(
        upload_to='videos/1080p/', null=True, blank=True, max_length=255)

    # HLS manifests and segments - neue Felder für HLS-Streaming
    hls_180p_manifest = models.FileField(
        upload_to='videos/hls/180p/', null=True, blank=True, max_length=255)
    hls_360p_manifest = models.FileField(
        upload_to='videos/hls/360p/', null=True, blank=True, max_length=255)
    hls_720p_manifest = models.FileField(
        upload_to='videos/hls/720p/', null=True, blank=True, max_length=255)
    hls_1080p_manifest = models.FileField(
        upload_to='videos/hls/1080p/', null=True, blank=True, max_length=255)

    upload_date = models.DateTimeField(auto_now_add=True)

    GENRE_CHOICES = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('documentary', 'Documentary'),
        ('horror', 'Horror'),
        ('sci-fi', 'Science Fiction'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ('animation', 'Animation'),
        ('fantasy', 'Fantasy'),
    ]
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)

    def __str__(self):
        return self.title

    @property
    def category(self):
        """Map genre to category for API compatibility."""
        return self.genre.title()