import os
import subprocess
from django.core.files import File
from django.conf import settings
from celery import shared_task
from .models import Video


@shared_task
def convert_video_resolutions(video_id):
    try:
        video = Video.objects.get(id=video_id)
        base_path = video.video_file.path
        filename = os.path.splitext(os.path.basename(base_path))[0]

        resolutions = {
            "video_1080p": "1920x1080",
            "video_720p": "1280x720",
            "video_480p": "854x480",
        }

        for field, res in resolutions.items():
            output_path = os.path.join(settings.MEDIA_ROOT, f"tmp/{filename}_{res}.mp4")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            cmd = [
                "ffmpeg",
                "-i", base_path,
                "-vf", f"scale={res}",
                "-c:a", "copy",
                output_path
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Speichere das File ins richtige Feld
            with open(output_path, "rb") as f:
                django_file = File(f)
                getattr(video, field).save(f"{filename}_{res}.mp4", django_file, save=False)

            os.remove(output_path)

        video.save()

    except Video.DoesNotExist:
        pass
