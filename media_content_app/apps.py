from django.apps import AppConfig


class MediaContentAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'media_content_app'

    def ready(self):
        import media_content_app.signals