import os

from celery import Celery

from ShortenYourLinkDjangoRest.task import test

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'ShortenYourLinkDjangoRest.settings'
)

CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

app = Celery(
    'ShortenYourLinkDjangoRest',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'test': {
        'task': "test",
        'schedule': 15
    }
}


@app.task(name="show", bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
