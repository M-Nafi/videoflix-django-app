import os
from celery import Celery

# Setze das Default Django-Settings-Modul für Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoflix_app.settings')

app = Celery('videoflix_app')

# Nimmt alle Einstellungen aus Django unter dem CELERY-Namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatisch alle tasks.py Dateien in deinen Apps finden
app.autodiscover_tasks()
