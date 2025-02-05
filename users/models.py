from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class RolesUser(models.Model):
    role_name = models.CharField(max_length=120)
    description = models.TextField()
    def __str__(self):
        return self.role_name
class User(AbstractUser):
    status = models.CharField(max_length=50, null=True, blank=True)  # Статус пользователя
    position = models.ForeignKey("Positions", on_delete=models.SET_NULL, null=True)  # Связь с должностью
    date_of_birth = models.DateField(null=True, blank=True)  # Дата рождения
    address = models.TextField(null=True, blank=True)  # Адрес
    department = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True)  # Связь с отделом
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)  # Телефон
    # telegram_id = models.CharField(max_length=20, unique=True, null=True, blank=True) #telegrma
    is_verified = models.BooleanField(default=False)  # Подтвержден ли пользователь
    on_vacation = models.BooleanField(default=False)  # В отпуске ли пользователь
    company = models.ForeignKey("Company",max_length=255, null=True, blank=True, on_delete=models.SET_NULL)  # Название компании

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Company(models.Model):
    company_name = models.CharField(max_length=120)
    has_admin = models.BooleanField(default=False)
    def __str__(self):
        return self.company_name

class Positions(models.Model):
    position_name = models.CharField(max_length=120)
    def __str__(self):
        return self.position_name

class Department(models.Model):
    department_name = models.CharField(max_length=120)
    department_head = models.CharField(max_length=120)
    def __str__(self):
        return self.department_name
