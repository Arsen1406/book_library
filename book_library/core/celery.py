import os
from celery import Celery
from book_library import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_library.settings')

app = Celery('SEND_EMAIL')

app.config_from_object("django.conf:settings", namespace='CELERY')
app.conf.timezone = settings.TIME_ZONE

app.autodiscover_tasks(packages=['core'])
