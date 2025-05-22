from django.contrib import admin
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    readonly_fields = ('video_1080p', 'video_720p', 'video_480p')
    fields = ('title', 'video_file', 'video_1080p', 'video_720p', 'video_480p')


