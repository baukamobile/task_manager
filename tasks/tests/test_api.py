
from django.test import TestCase
from rest_framework.test import APITestCase
from users.models import User
from django.utils.timezone import now
import datetime
from tasks.models import Task, Projects, Status, Priority, Department


class TaskApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(first_name="testuser")
        self.department = Department.objects.create(department_name="IT")

        self.project = Projects.objects.create(
            project_name="Test Project",
            department=self.department,
            end_date=now() + datetime.timedelta(days=30)
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


class StatusApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(first_name="testuser")
        self.department = Department.objects.create(
            department_name = "some department",
            department_head = self.user
        )
        self.project = Projects.objects.create(
            project_name="Test Project",
            description="some description",
            department=self.department,
            assigned = self.user,
            end_date=now() + datetime.timedelta(days=30)
        )
        self.status = Status.objects.create(status_name='to delete', project=self.project)

    def test_get_status_list(self):
        print('status test начинается')
        response = self.client.get('/tasks/status/')
        print("📢 Status API:", response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class ProjectsApiTestApi(APITestCase):
    def setUp(self):
        self.assigned = User.objects.create(first_name='Some User')
        self.department = Department.objects.create(department_name="IT")
        self.project = Projects.objects.create(
            project_name="Some Project",
            description="Some description",
            department=self.department,
            assigned= self.assigned,
            start_date=now() + datetime.timedelta(days=8),
            end_date=now() + datetime.timedelta(days=20),
        )

    def test_get_projects_list(self):
        response = self.client.get('/tasks/projects/')
        print("📢 Проекты API:", response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
