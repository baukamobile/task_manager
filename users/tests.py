from django.contrib.gis.db.backends.postgis.const import BANDTYPE_PIXTYPE_MASK
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APITestCase
from users.models import User,Positions,Roles,Department,Company
# Create your tests here.
from django.utils.timezone import now

class UserTests(TestCase):
    def setUp(self):
        self.position = Positions.objects.create(position_name="Cashier")
        self.role = Roles.objects.create(role_name="Исполнитель")
        self.department = Department.objects.create(department_name='Guidejet')
        self.company = Company.objects.create(company_name='Onay')

        self.user = User.objects.create(
            email = 'test7@gmail.com',
            phone_number = '7758996545',
            first_name = 'test7',
            last_name='test7',
            status = User.ACTIVE,
            position=self.position,
            role_user=self.role,
            date_of_birth=now(),
            address='123 Main St.',
            department=self.department,
            telegram_id='123456789',
            is_verified=True,
            on_vacation=True,
            company=self.company,
            is_superuser=False,
            is_active=True,
            is_owner=False,
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test7@gmail.com')
        self.assertEqual(self.user.first_name, 'test7')
        self.assertEqual(self.user.last_name,'test7')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_superuser)

    def test_str_representation(self):
        self.assertEqual(str(self.user),'test7')

    def test_required_field(self):
        user = User(email='test7@gmail.com',first_name='test10')
        with self.assertRaises(ValidationError):
            user.full_clean()
    def test_unique_email(self):
        with self.assertRaises(Exception):
            User.objects.create(email='unique@gmail.com',first_nsme='test754')

    def test_default_values(self):
        user=User.objects.create(email='default@gmail.com',first_name='Deafault')
        self.assertFalse(user.is_verified)
        self.assertFalse(user.on_vacation)
        self.assertTrue(user.is_active)


class PositionsApiTest(APITestCase):
    def setUp(self):
        self.position = Positions.objects.create(position_name="Cashier",)
    def test_get_position_list(self):
        print('postition test начинается')
        response = self.client.get('/users/positions/')
        print('Position API:', response.json())
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()),1)


class CompanyApiTest(APITestCase):
    def setUp(self):
        self.director = User.objects.create(first_name='Cannady')
        self.company = Company.objects.create(company_name='Kegoc')
    def test_get_company_list(self):
        response = self.client.get('/users/company/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()),1)

class DepartmentApiTest(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(
            department_name = 'GuideJet',
            department_head = 'Bill Gates',
            deactivate = True,
        )
    def test_get_department_list(self):
        response = self.client.get('/users/department/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()),1)

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




