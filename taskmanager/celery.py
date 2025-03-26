import os
from celery import Celery # Importing Celery from the celery package

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings') # Set the settings  module  to the settings     module
app = Celery('taskmanager') # Application
app.config_from_object('django.conf:settings', namespace='CELERY') # Load the configuration from the settings module
app.autodiscover_tasks(['tasks','users','event_calendar']) # Enable
app.conf.update( # Additional settings
    worker_concurrency=1,  # Ограничиваем количество воркеров (Windows не любит много процессов)
    worker_prefetch_multiplier=1,  # Минимизируем загрузку процессов
)
# celery -A taskmanager worker --pool=solo --loglevel=info
# (.venv) PS C:\Users\User\Desktop\docs\taskmanager> celery -A taskmanager.celery worker --pool=solo -l INFO

#чтобы запускать мониторинг celery flower
#(.venv) PS C:\Users\User\Desktop\docs\taskmanager> celery -A taskmanager.celery flower --port=5555