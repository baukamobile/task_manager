from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Permission
from simple_history.models import HistoricalRecords


import logging
from django.contrib.auth.models import Permission

# Create your models here.
class Roles(models.Model): #роли пользователи
    role_name = models.CharField(max_length=120)
    description = models.TextField()
    # permissions = models.ForeignKey(Permission,on_delete=models.SET_NULL,null=True, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)  # Связь с правами Django
    def __str__(self):
        return self.role_name
    class Meta:
        verbose_name_plural = 'Roles'

class UserCustomManager(BaseUserManager):
    # Указываем, что этот менеджер будет использоваться при миграциях
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        """
        Вспомогательная функция для создания пользователя с паролем и телефонным номером.
        Проверяет наличие телефонного номера, создает нового пользователя с переданными
        дополнительными полями и сохраняет его в базе данных.
        :param phone_number: Телефонный номер пользователя (обязателен).
        :param password: Пароль пользователя (обязателен).
        :param extra_fields: Дополнительные поля, передаваемые для создания пользователя.
        :return: Сохранённый объект пользователя.
        """
        if not phone_number:
            raise ValueError('The given phone number must be set')  # Проверка на обязательность телефонного номера
        user = self.model(phone_number=phone_number, **extra_fields)  # Создаём пользователя с дополнительными полями
        user.set_password(password)  # Устанавливаем пароль с хешированием
        user.save(using=self._db)  # Сохраняем пользователя в базе данных
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Создаёт обычного пользователя с переданным телефонным номером и паролем.
        По умолчанию назначаются флаги `is_staff=False` и `is_superuser=False`.

        :param phone_number: Телефонный номер пользователя (обязателен).
        :param password: Пароль пользователя (необязателен).
        :param extra_fields: Дополнительные поля, передаваемые для создания пользователя.
        :return: Объект созданного пользователя.
        """
        extra_fields.setdefault('is_staff', False)  # Если не указано, считаем, что пользователь не является сотрудником
        extra_fields.setdefault('is_superuser', False)  # Если не указано, считаем, что пользователь не является суперпользователем
        return self._create_user(phone_number, password, **extra_fields)  # Создаём пользователя через вспомогательную функцию

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Создаёт суперпользователя с переданным телефонным номером и паролем.
        По умолчанию назначаются флаги `is_staff=True` и `is_superuser=True`.

        :param phone_number: Телефонный номер суперпользователя (обязателен).
        :param password: Пароль суперпользователя (необязателен).
        :param extra_fields: Дополнительные поля, передаваемые для создания суперпользователя.
        :raises ValueError: Если `is_staff` или `is_superuser` не установлены в `True`, генерируется исключение.
        :return: Объект созданного суперпользователя.
        """
        extra_fields.setdefault('is_staff', True)  # Суперпользователь обязательно является сотрудником
        extra_fields.setdefault('is_superuser', True)  # Суперпользователь обязательно является суперпользователем
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')  # Ошибка, если не установлен флаг is_staff
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')  # Ошибка, если не установлен флаг is_superuser
        return self._create_user(phone_number, password, **extra_fields)  # Создаём суперпользователя через вспомогательную функцию


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    ACTIVE = 'active'
    FIRED = 'fired' #STATUS USER
    STATUS_CHOICES = [
        (ACTIVE, 'АКТИВЕН'),
        (FIRED, 'УВОЛЕН'),
    ]
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)  # Можно оставить телефон, но как дополнительный параметр
    # phone_number =
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(unique=True,blank=True)  # Сделаем email обязательным и уникальным
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, null=True, blank=True)
    position = models.ForeignKey("Positions", on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="position_employees")
    role_user = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='role_employees')
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    department = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True, blank=True,related_name='department_employees')
    telegram_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False) #пользователь подвержден?
    on_vacation = models.BooleanField(default=False) #в отпуске?
    company = models.ForeignKey("Company", on_delete=models.SET_NULL, null=True, blank=True,related_name='company_employees')
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_owner = models.BooleanField(default=False) #владееть компании?
    image = models.ImageField(upload_to='Users_avatar', blank=True, null=True)
    background_profile_image = models.ImageField(upload_to='Users_background_images', blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    history = HistoricalRecords() #simple history
    USERNAME_FIELD = 'email'  # Используем email для входа
    REQUIRED_FIELDS = ['phone_number', 'first_name']  # Добавляем только необходимые поля

    objects = UserCustomManager()

    def __str__(self):
        return self.first_name
    def get_permissions(self):
        """Возвращает список всех прав, доступных пользователю через его роль"""
        if self.role_user:
            return self.role_user.permissions.all()
        return []

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role_user:
            self.set_permissions_from_role()

    def set_permissions_from_role(self):
        # права юзер к ролью
        if self.role_user:
            self.user_permissions.set(self.role_user.permissions.all())
    def has_perm(self,perm,obj=None):
        """Проверяем, есть ли у пользователя право (учитываем роль)"""
        if self.is_superuser: #если админ возвращаем что он и есть
            return True
        if self.role_user: # если не админ возвращаем все его/ее права
            return self.role_user.permissions.filter(codename=perm).exists()
        return False
    class Meta:
        ordering = ['-date_joined']
        verbose_name_plural = 'users'

class Company(models.Model):
    company_name = models.CharField(max_length=120)
    director = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='director_company') #директор
    def __str__(self):
        return self.company_name
    # has_admin = models.BooleanField(default=False)
    def __str__(self):
        return self.company_name
    class Meta:
        verbose_name_plural='Company'



class Positions(models.Model):
    position_name = models.CharField(max_length=120,unique=True)
    department = models.ForeignKey('Department',on_delete=models.CASCADE,related_name='positions',null=True,blank=True)
    class Meta:
        verbose_name_plural='Positions'
    def __str__(self):
        return f'{self.position_name, self.department}'

class ActiveDepartmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deactivate=False)

class Department(models.Model):
    department_name = models.CharField(max_length=120)
    department_head = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name="header_departments")
    # department_head_name = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True,
                                             # related_name="header_departments")
    deactivate = models.BooleanField(default=False)
    objects = models.Manager()
    activate = ActiveDepartmentManager()

    def __str__(self):
        return self.department_name

    def save(self, *args, **kwargs):
        first_save = self.pk is None  # Проверка, новый ли это объект
        super().save(*args, **kwargs)  # Сначала сохраняем департамент

        # Обновляем пользователей, если это не первое сохранение
        if not first_save:
            if self.deactivate:
                # Отключаем всех, кроме суперюзеров и владельцев
                User.objects.filter(
                    department=self,
                    is_superuser=False,
                    is_owner=False
                ).update(is_active=False)
            else:
                # Включаем только активных, исключая суперюзеров и владельцев
                User.objects.filter(
                    department=self,
                    status=User.ACTIVE,
                    is_superuser=False,
                    is_owner=False
                ).update(is_active=True)




class GrafanaDashboard(models.Model):
    name = models.CharField(max_length=255)  # Название дашборда
    dashboard_uid = models.CharField(max_length=100, unique=True)  # UID дашборда в Grafana
    panel_id = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.name
