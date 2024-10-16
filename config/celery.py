from __future__ import absolute_import
import os
from celery import Celery
from celery import schedules

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('khadipro')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
