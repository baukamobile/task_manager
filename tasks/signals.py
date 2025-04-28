# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from tasks.models import Task
# from django.apps import AppConfig
# from django.core.signals import setting_changed
#
#
# def my_callback(sender, **kwargs):
#     print('Setting changed!')

# @receiver(post_save, sender=Task)
# def task_created(sender, instance, created, **kwargs):
#     if created:
#         print(f'Новая задача создан {instance.task_name}')

