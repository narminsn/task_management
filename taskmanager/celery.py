from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')

app = Celery('taskmanager')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    # BROKER_URL='amqp://root:12345@127.0.0.1:15672//',
    CELERY_DISABLE_RATE_LIMITS=True,
    CELERY_ACCEPT_CONTENT=['json', ],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-1-seconds': {
        'task': 'task_app.tasks.send_mail',
        'schedule': crontab(),
        'args': ()
    },
}

# app.conf.beat_schedule = {
#     'add-every-1-seconds': {
#         'task': 'news.tasks.get_name',
#         'schedule': 1,
#         'args': ()
#     },
# }