from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config',
             broker=settings.BROKER,
             backend='rpc://',
             include=['config.task'])

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.update(
    task_serializer='json',
    result_serializer='json',
    timezone = 'Asia/Seoul',
    task_acks_late = True,
    broker_heartbeat=0
)
