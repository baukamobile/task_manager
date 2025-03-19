from django.contrib.gis.db.backends.postgis.const import BANDTYPE_PIXTYPE_MASK
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APITestCase
from django.utils import timezone
from users.models import User,Positions,Roles,Department,Company

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
            date_of_birth=timezone.now(),
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
        user = User(email='test9@gmail.com',first_name='test7')
        with self.assertRaises(ValidationError):
            user.full_clean()
    # def test_unique_email(self):
    #     with self.assertRaises(Exception):
    #         User.objects.create(email='unique3@gmail.com',first_name='test754')

    def test_default_values(self):
        user=User.objects.create(email='default@gmail.com',first_name='Deafault',phone_number='1234567890',)
        self.assertFalse(user.is_verified)
        self.assertFalse(user.on_vacation)
        self.assertTrue(user.is_active)
#
class CompanyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

    # def setUp(self):
        cls.director = User.objects.create_user(email="test@gmail.com",first_name='Albert',phone_number=1651515)
        cls.company = Company.objects.create(
            company_name = 'some company',
            director = cls.director
        )
    def test_company_creation(self):
        self.company = Company.objects.get(id=self.company.id)
        self.assertEqual(self.company.company_name,'some company')
        self.assertEqual(self.company.director.first_name,'Albert')
    def test_company_str(self):
        self.assertEqual(str(self.company),'some company')

#
class PositionsModelTest(TestCase):
    def setUp(self):
        self.position = Positions.objects.create(
            position_name = "some position"
        )
    def test_position_creation(self):
        self.assertEqual(self.position.position_name, 'some position')
    def test_position_str(self):
        self.assertEqual(str(self.position), 'some position')


class DepartmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email="test@gmail.com",first_name='Albert',phone_number=1651515)
        cls.department = Department.objects.create(
            department_name="some department",
            department_head=cls.user,
            deactivate=False
        )

    def test_department_creation(self):
        # Проверяем создание без лишнего запроса
        self.assertEqual(self.department.department_name, "some department")
        self.assertEqual(self.department.department_head.first_name, 'Albert')  # Проверяем объект, а не имя
        self.assertFalse(self.department.deactivate)  # False вместо сравнения с False

    def test_department_str(self):
        # Проверяем метод __str__
        self.assertEqual(str(self.department), "some department")

    def test_save_deactivate_users(self):
        # Проверяем логику save() при deactivate=True
        user1 = User.objects.create_user(email="test3@gmail.com",phone_number=1659915,first_name="user1", department=self.department, is_active=True)
        user2 = User.objects.create_user(email="test1@gmail.com",phone_number=1651505,first_name="user2", department=self.department, is_active=True, is_superuser=True)

        self.department.deactivate = True
        self.department.save()

        user1.refresh_from_db()
        user2.refresh_from_db()
        self.assertFalse(user1.is_active)  # Обычный пользователь отключён
        self.assertTrue(user2.is_active)  # Суперюзер остался активным

    def test_save_activate_users(self):
        # Проверяем логику save() при deactivate=False
        user1 = User.objects.create_user(email="test2@gmail.com",phone_number=1653515,first_name="user1", department=self.department, is_active=False, status=User.ACTIVE)
        user2 = User.objects.create_user(email="test12@gmail.com",phone_number=1681515,first_name="user2", department=self.department, is_active=False)

        self.department.deactivate = False
        self.department.save()

        user1.refresh_from_db()
        user2.refresh_from_db()
        self.assertTrue(user1.is_active)  # Активный статус — включён
        self.assertFalse(user2.is_active)  # Нет статуса ACTIVE — остался выключенным


