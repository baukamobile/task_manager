from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from tasks.views import *
import datetime
from .models import Task, Projects, Status, Priority, Department

User = get_user_model()


class TaskModelTest(TestCase):
    def setUp(self):
        """Создаем тестовые данные перед каждым тестом"""
        self.user = User.objects.create(first_name="testuser")
        self.department = Department.objects.create(department_name="IT")

        self.project = Projects.objects.create(
            project_name="Test Project",
            department=self.department,
            end_date=now() + datetime.timedelta(days=30)
        )

        self.status = Status.objects.create(status_name="In Progress", user=self.user)
        self.priority = Priority.objects.create(priority_name="High", user=self.user)
        self.end_date = now() + datetime.timedelta(days=7)

        self.task = Task.objects.create(
            task_name="Test Task",
            description="Some description",
            projects=self.project,
            assigned=self.user,
            status=self.status,
            priority=self.priority,
            department=self.department,
            end_date=self.end_date,
        )

    def test_task_creation(self):
        """Проверяем, что задача создается"""
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(self.task.task_name, "Test Task")
        self.assertEqual(self.task.projects, self.project)

    def test_task_str(self):
        """Проверяем, что __str__ выводит название задачи"""
        self.assertEqual(str(self.task), "Test Task")

class TaskApiTest(APITestCase):
    def setUp(self):
        """Создаем тестовые данные перед каждым тестом"""
        self.user = User.objects.create(first_name="testuser")
        self.department = Department.objects.create(department_name="IT")

        self.project = Projects.objects.create(
            project_name="Test Project",
            department=self.department,
            end_date=now() + datetime.timedelta(days=30)
        )

        self.status = Status.objects.create(status_name="In Progress", user=self.user)
        self.priority = Priority.objects.create(priority_name="High", user=self.user)
        self.end_date = now() + datetime.timedelta(days=7)

        self.task = Task.objects.create(
            task_name="Test Task",
            description="Some description",
            projects=self.project,
            assigned=self.user,
            status=self.status,
            priority=self.priority,
            department=self.department,
            end_date=self.end_date,
        )
    def test_task_get_list(self):
        response = self.client.get('/tasks/tasks/')  # Убедись, что URL правильный
        print("📢 Ответ API:", response.json())  # Посмотреть, что реально возвращается
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)  # Теперь в базе есть 1 задача


class StatusApitTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(first_name="testuser")
        self.status_name = Status.objects.create(status_name='to delete',user=self.user)

    def test_get_status_list(self):
        print('status test начинается')
        response = self.client.get('/tasks/status/')
        print("📢 Status API:", response.json())
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data),1)
        print("📢 Status API:", response.json())
