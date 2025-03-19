from django.contrib.gis.db.backends.postgis.const import BANDTYPE_PIXTYPE_MASK
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APITestCase
from users.models import User,Positions,Roles,Department,Company
# Create your tests here.
from django.utils.timezone import now



'''
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
    date_joined = models.DateTimeField(default=timezone.now)
    history = HistoricalRecords()

    USERNAME_FIELD = 'email'  # Используем email для входа
    REQUIRED_FIELDS = ['phone_number', 'first_name']  # Добавляем только необходимые поля

    objects = UserCustomManager()

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
'''




