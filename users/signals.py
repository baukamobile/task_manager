from django.apps import AppConfig
from django.core.signals import setting_changed

def my_callback(sender, **kwargs):
    print('setting changed')

class MyAppConfig(AppConfig):
    def ready(self):
        setting_changed.connect(my_callback)