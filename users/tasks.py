from celery import shared_task
from django.core.mail import send_mail
import environ
from pathlib import Path
env = environ.Env()
environ.Env.read_env()
# @shared-task
# def send_email()

@shared_task
def send_mail_message(user_email):
    send_mail(
        subject='Добро пожаловать!',
        message='Спасибо за регистрацию! Администратор подтвердит ваш email.',
        from_email=env(EMAIL_HOST_USER),  # Проверь, что email правильный
        recipient_list=[user_email],  # Должен быть список
        fail_silently=False,
    )
    return f'Email sent to {user_email}'




