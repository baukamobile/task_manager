from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

# Create your models here.
class RolesUser(models.Model):
    role_name = models.CharField(max_length=120)
    description = models.TextField()
    # permissions = models.ManyToManyField('Permissions', blank=True)
    def __str__(self):
        return self.role_name

class Permissions(models.Model):
    role_id = models.ForeignKey(RolesUser, on_delete=models.CASCADE)
    permission_name = models.CharField(max_length=120)
    permission_description = models.TextField()
    def __str__(self):
        return self.permission_name
class UserCustomManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError('The given phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(phone_number, password, **extra_fields)

class User(AbstractUser):
    username = None  # Убираем username
    first_name = None  # Убираем first_name
    last_name = None  # Убираем last_name
    ACTIVE = 'active'
    FIRED = 'fired' #STATUS USER
    STATUS_CHOICES = [
        (ACTIVE, 'АКТИВЕН'),
        (FIRED, 'УВОЛЕН'),
    ]
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)  # Можно оставить телефон, но как дополнительный параметр
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)  # Сделаем email обязательным и уникальным
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, null=True, blank=True)
    position = models.ForeignKey("Positions", on_delete=models.SET_NULL, null=True, blank=True)
    role_user = models.ForeignKey(RolesUser, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    department = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True, blank=True)
    telegram_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    on_vacation = models.BooleanField(default=False)
    company = models.ForeignKey("Company", on_delete=models.SET_NULL, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_owner = models.BooleanField(default=False)
    image = models.ImageField(blank=True, null=True)
    background_profile_image = models.ImageField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    history = HistoricalRecords() #simple history
    USERNAME_FIELD = 'email'  # Используем email для входа
    REQUIRED_FIELDS = ['phone_number', 'first_name']  # Добавляем только необходимые поля

    objects = UserCustomManager()

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role_user:
            self.set_permissions_from_role()

    def set_permissions_from_role(self):
        # права юзер к ролью
        if self.role_user:
            self.user_permissions.set(self.role_user.permissions.all())

    class Meta:
        ordering = ['-date_joined']
        verbose_name_plural = 'users'



class Company(models.Model):
    company_name = models.CharField(max_length=120)
    has_admin = models.BooleanField(default=False)
    def __str__(self):
        return self.company_name
    class Meta:
        verbose_name_plural='Company'

class Positions(models.Model):
    position_name = models.CharField(max_length=120)
    def __str__(self):
        return self.position_name
    class Meta:
        verbose_name_plural='Positions'

class Department(models.Model):
    department_name = models.CharField(max_length=120)
    department_head = models.CharField(max_length=120)
    def __str__(self):
        return self.department_name

#
# SELECT pg_terminate_backend(pg_stat_activity.pid)
# FROM pg_stat_activity
# WHERE pg_stat_activity.datname = 'manager';