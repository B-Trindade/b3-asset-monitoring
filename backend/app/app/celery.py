"""
Send tasks to Celery through Redis message broker.
"""

import os

from celery import Celery


# Allows Celery service to initiate django settings from backendapp
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery("app")
app.config_from_object("django.conf:settings", namespace="CELERY")


@app.task
def app_task():
    return "App task called."


app.autodiscover_tasks()
