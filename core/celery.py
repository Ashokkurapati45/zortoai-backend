# core/celery.py
import os
from celery import Celery

# Point Celery to Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# Read Celery settings from Django settings, all keys starting with CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks.py in all installed apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
