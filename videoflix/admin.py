from django.contrib import admin
from .models import Video, VideoProgress

class VideoProgressInline(admin.TabularInline):
    """
    Inline admin for VideoProgress to show progress per user directly on Video admin page.
    """
    model = VideoProgress
    extra = 0
    readonly_fields = ('position_in_seconds', 'updated_at')
    raw_id_fields = ('user',)  # changed: use raw ID widget for User relation

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """
    Admin interface for the Video model.
    """
    list_display = ('title', 'genre', 'upload_date')  # changed: sichtbar in der Listenansicht
    search_fields = ('title', 'description')          # changed: Suche nach Titel und Beschreibung
    list_filter = ('genre', 'upload_date')            # changed: Filtermöglichkeiten
    inlines = (VideoProgressInline,)                  # changed: Fortschritt inline anzeigen

@admin.register(VideoProgress)
class VideoProgressAdmin(admin.ModelAdmin):
    """
    Admin interface for the VideoProgress model.
    """
    list_display = ('user', 'video', 'position_in_seconds', 'updated_at')  # changed
    search_fields = ('user__email', 'video__title')                        # changed
    list_filter = ('updated_at',)                                          # changed
    raw_id_fields = ('user', 'video')  # changed: schnelle Auswahl per ID
