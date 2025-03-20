from celery import shared_task
from django.core.mail import send_mail
import environ
from pathlib import Path
env = environ.Env()
environ.Env.read_env()
@shared_task
def add(x, y):
    return x + y

@shared_task
def multiply(x, y):
    return x*y
@shared_task
def subtract(q,w):
    return q - w

@shared_task
def sorting(n):
    for i in range(len(n)):
        for j in range(len(n)-i-1):
            if n[j] > n[j+1]:  # Если текущий элемент больше следующего, меняем местами
                n[j], n[j+1] = n[j+1], n[j]
    print(n)

