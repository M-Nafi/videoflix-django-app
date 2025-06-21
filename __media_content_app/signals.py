from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Video
from .services.__tasks import convert_video_resolutions

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        convert_video_resolutions.delay(instance.id)
