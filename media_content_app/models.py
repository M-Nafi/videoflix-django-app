from django.db import models
from django.contrib.auth.models import User


class Video(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='media/videos/') 
    thumbnail = models.FileField(upload_to='media/thumbnails/')  
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=50, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

