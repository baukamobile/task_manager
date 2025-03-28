from celery import shared_task
from django.core.mail import send_mail
import requests
from django.apps import apps
import json
import environ
from pathlib import Path
env = environ.Env()
environ.Env.read_env()

@shared_task
def send_mail_message(user_id):
    """Отправка email после регистрации"""
    User = apps.get_model('users','User')
    try:
        user = User.objects.get(id=user_id)
        send_mail(
            subject='Добро пожаловать!',
            message=f'Спасибо за регистрацию {user.first_name}! Администратор подтвердит ваш email.',
            from_email=env('EMAIL_HOST_USER'),  # Проверька эмейл
            recipient_list=[user.email],  # Должен быть список
            fail_silently=False,
        )
        return f'Email sent to {user.email}'
    except Exception as e:
        return f' Ошибка при отправке сообщение на почту: {e}'


# @shared_task
# def periodic_send_mail(user_id):
#     """Celery: Отправка email только вошедшему пользователю"""
#     User = apps.get_model('users', 'User')
#     try:
#         user = User.objects.get(id=user_id)
#         send_mail_message.delay(user.id)  # Отправляем письмо
#         return f'Email отправлен пользователю {user.email}'
#     except User.DoesNotExist:
#         return f'Ошибка: пользователь с id={user_id} не найден'
@shared_task
def send_mail_to_logged_user(user_id):
    """Celery: Отправка email конкретному пользователю"""
    User = apps.get_model('users', 'User')
    try:
        user = User.objects.get(id=user_id)
        send_mail_message.delay(user.id)
        return f'Email отправлен пользователю {user.email}'
    except User.DoesNotExist:
        return f'Ошибка: пользователь с id={user_id} не найден'

@shared_task(ignore_result=True)
def square(x,y):
    return x**y


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