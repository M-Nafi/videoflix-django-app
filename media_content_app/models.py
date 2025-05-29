from django.db import models
from django.conf import settings


class Video(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/originals/')  # Nur dieses Feld wird manuell hochgeladen
    thumbnail = models.FileField(upload_to='thumbnails/')
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=50, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Automatisch erstellte Versionen
    video_1080p = models.FileField(upload_to='videos/1080p/', null=True, blank=True)
    video_720p = models.FileField(upload_to='videos/720p/', null=True, blank=True)
    video_360p = models.FileField(upload_to='videos/360p/', null=True, blank=True)
    video_120p = models.FileField(upload_to='videos/120p/', null=True, blank=True)

    def __str__(self):
        return self.title


class VideoProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    last_position = models.FloatField(default=0.0)  # in Sekunden z. B.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'video')  # Jeder User darf nur einen Fortschritt pro Video haben
