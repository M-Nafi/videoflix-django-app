from django.contrib import admin
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    readonly_fields = ('video_1080p', 'video_720p', 'video_480p')
    fields = ('title', 'video_file', 'description', 'thumbnail', 'genre')

    def save_model(self, request, obj, form, change):
        if not change:  
            obj.owner = request.user
        obj.save()



