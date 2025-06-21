# import os
# from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# app = Celery('core')

# # Nimmt alle Einstellungen aus Django unter dem CELERY-Namespace
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Automatisch alle tasks.py Dateien in deinen Apps finden
# app.autodiscover_tasks()
