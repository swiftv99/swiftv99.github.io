import os
from celery import Celery
from iclean import celeryconfig


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iclean.settings')

app = Celery('iclean')

app.config_from_object(celeryconfig)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
