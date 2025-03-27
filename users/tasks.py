from celery import shared_task
from django.core.mail import send_mail
import requests
from django.apps import apps
import json
import environ
from pathlib import Path
env = environ.Env()

environ.Env.read_env()
# @shared-task
# def send_email()
# from django.contrib.auth import get_user_model
# User = get_user_model()

@shared_task
def send_mail_message(user_id):
    """Отправка email после регистрации"""
    User = apps.get_model('users','User')
    try:
        user = User.objects.get(id=user_id)
        send_mail(
            subject='Добро пожаловать!',
            message=f'Спасибо за регистрацию {user.first_name}! Администратор подтвердит ваш email.',
            from_email=env('EMAIL_HOST_USER'),  # Проверь, что email правильный
            recipient_list=[user.email],  # Должен быть список
            fail_silently=False,
        )

        return f'Email sent to {user.email}'
    except Exception as e:
        return f' Ошибка при отправке сообщение на почту: {e}'
@shared_task(ignore_result=True)
def square(x,y):
    return x*y

# @shared_task
# def fetch_weather():
#     response = requests.get(f'https://wise.com/ru/currency-converter/usd-to-eur-rate')
#     return response.json

@shared_task
def featching():
    url = 'https://wise.com/ru/currency-converter/usd-to-eur-rate'
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        return f'Error is {e}'