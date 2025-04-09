from django.apps import AppConfig
from django.core.signals import setting_changed

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
    # def ready(self):
    #     # setting_changed.connect(my_ca)
    #     import tasks.signals  # noqa