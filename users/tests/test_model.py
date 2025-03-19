from django.contrib.gis.db.backends.postgis.const import BANDTYPE_PIXTYPE_MASK
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APITestCase
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
