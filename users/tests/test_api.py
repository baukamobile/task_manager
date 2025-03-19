
from django.test import TestCase
from rest_framework.test import APITestCase
from users.models import User,Positions,Roles,Department,Company


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
