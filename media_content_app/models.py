from django.db import models
from django.contrib.auth.models import User


class Video(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='videos/originals/') 
    thumbnail = models.FileField(upload_to='thumbnails/')  
    description = models.TextField(blank=True)
    hls_master_playlist = models.FileField(upload_to='videos/hls/', blank=True, null=True)
    genre = models.CharField(max_length=50, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

