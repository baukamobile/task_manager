from pydoc import describe

from django.utils import timezone
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import now

import datetime
from tasks.models import Task, Projects, Status, Priority, Department
from tasks.serializers import StatusSerializer, ProjectSerializer
from users.models import User
# from rest_framework.status import st

class TaskApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(first_name="testuser")
        self.department = Department.objects.create(department_name="IT")
        self.project = Projects.objects.create(
            project_name="Test Project",
            department=self.department,
            end_date=now() + datetime.timedelta(days=30),
            assigned=self.user
        )
        self.status = Status.objects.create(status_name="In Progress", project=self.project)
        self.priority = Priority.objects.create(priority_name="High")
        self.end_date = now() + datetime.timedelta(days=7)

        self.task = Task.objects.create(
            task_name="Test Task",
            description="Some description",
            project=self.project,
            assigned=self.user,
            status=self.status,
            priority=self.priority,
            department=self.department,
            end_date=self.end_date,
        )

    def test_task_get_list(self):
        response = self.client.get('/tasks/tasks/')
        print("📢 Ответ API:", response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

class StatusViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email="test@gmail.com", password='password$rT', phone_number=5615132)
        cls.department = Department.objects.create(department_name="koko", department_head=cls.user)
        cls.project = Projects.objects.create(
            project_name="test project",
            end_date=timezone.now(),
            department=cls.department
        )
        cls.status1 = Status.objects.create(status_name="in progress", project=cls.project)
        cls.status2 = Status.objects.create(status_name="to delete", project=cls.project)

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_status_list(self):
        url = reverse('status-list')  #
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  #

        expected_data = StatusSerializer([self.status1, self.status2], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_status_list_filtered_by_project(self):
        url = reverse('status-list')  #
        response = self.client.get(f'{url}?project={self.project.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  #

class ProjectsViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email="test@gmail.com", password='password$rT', phone_number=5615132)
        cls.department = Department.objects.create(department_name="koko", department_head=cls.user)
        cls.projects = Projects.objects.create(
            project_name="some project",
            description="some description",
            department=cls.department,
            # start_date=timezone.now(),
            assigned=cls.user,
            # end_date="2025-03-29 11:43:34.592878+00"
            end_date=timezone.now()
        )
        cls.projects1 = Projects.objects.create(project_name="some project",description="some description",
                                                department=cls.department,assigned=cls.user,end_date=timezone.now()
                                                )
        cls.projects2 = Projects.objects.create(project_name="some project2", description="some description2",
                                                department=cls.department, assigned=cls.user, end_date=timezone.now()
                                                )

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_project_list(self):
        url = reverse('projects-list')
        response = self.client.get(url)

        # DEBUG: проверяем, что возвращает API
        print("API Response:", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Ожидаем 3 проекта

        # Генерируем ожидаемые данные и сортируем по ID, чтобы порядок не влиял
        expected_data = ProjectSerializer([self.projects, self.projects1, self.projects2], many=True).data
        expected_data = sorted(expected_data, key=lambda x: x["id"])
        response_data = sorted(response.data, key=lambda x: x["id"])

        self.assertEqual(response_data, expected_data)
# ([self.status1, self.status2], many=True).data
#         self.assertEqual(response.data, expected_data)


