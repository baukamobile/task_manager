from django.core.exceptions import ValidationError
from django.utils import timezone

from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from users.models import User,Department
import datetime
from tasks.models import Task, Projects, Status, Priority

class TaskModelTest(TestCase):
    def setUp(self):
        #Подготовка ланныз
        self.user = User.objects.create(first_name='Albert')
        self.department = Department.objects.create(department_name='department IT')
        self.project = Projects.objects.create(
            project_name='Develope trello clone',
            department = self.department,
            end_date = timezone.now()
        )
        self.status = Status.objects.create(
            status_name='In Process',
            project=self.project
        )
        self.priority= Priority.objects.create(priority_name='Low')
        self.task = Task.objects.create(
            task_name = "Task Name",
            description = "Test description",
            status = self.status,
            assigned = self.user,
            start_date=timezone.now(),
            end_date=timezone.now(),
            priority=self.priority,
            project=self.project,
            department=self.department
        )
    def test_task_creation(self):
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.task_name, "Task Name")
        self.assertEqual(task.description, 'Test description')
        self.assertEqual(task.status.status_name, 'In Process')
        self.assertEqual(task.assigned.first_name, 'Albert')
        self.assertEqual(task.project.project_name, 'Develope trello clone')
        self.assertEqual(task.priority.priority_name, 'Low')
        self.assertFalse(task.agreed_with_managers)

    def test_task_str(self):
        self.assertEqual(str(self.task),'Task Name')

    def test_task_clean_invalid_status(self):
        # Проверяем валидацию clean
        other_project = Projects.objects.create(
            project_name = "Other Project",
            department = self.department,
            end_date = timezone.now()
        )
        invalid_status = Status.objects.create(status_name="Done", project=other_project)
        self.task.status = invalid_status
        with self.assertRaises(ValidationError):
            self.task.clean()  # Должна быть ошибка, так как status.project != task.project
    def test_comments_count(self):
        from ..models import Task_comments
        Task_comments.objects.create(task=self.task,
        user=self.user, comment="Test Comment")
        self.assertEqual(self.task.comments_count(), 1)

class StatusModelTest(TestCase):
    def setUp(self):
        # self.department = Department.objects.create(name="Test Dept")
        self.project = Projects.objects.create(
            project_name="Test Project",
            department=Department.objects.create(department_name="Test Dept"),
            end_date=timezone.now()
        )
        self.status = Status.objects.create(status_name="In Progress", project=self.project)

    def test_status_creation(self):
        status = Status.objects.get(id=self.status.id)
        self.assertEqual(status.status_name, "In Progress")
        self.assertEqual(status.project.project_name, "Test Project")

    def test_status_str(self):
        self.assertEqual(str(self.status), "In Progress")

class PriorityModelTest(TestCase):
    def setUp(self):
        self.priority=Priority.objects.create(priority_name="Low")
    def test_priority_creation(self):
        priority = Priority.objects.get(id=self.priority.id)
        self.assertEqual(priority.priority_name, 'Low')
    def test_priority_str(self):
        self.assertEqual(str(self.priority),'Low')

class ProjectsModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(department_name='Development department')
        self.user = User.objects.create(first_name='Albert')
        self.projects = Projects.objects.create(
            project_name="Some project",
            description = "Some description",
            department = self.department,
            start_date = timezone.now(),
            assigned = self.user,
            end_date = timezone.now()
        )

    def test_projects_creation(self):
        projects = Projects.objects.get(id=self.projects.id)
        self.assertEqual(projects.project_name, 'Some project'),
        self.assertEqual(projects.description,'Some description'),
        self.assertEqual(projects.department.department_name,'Development department'),
        self.assertEqual(projects.assigned.first_name,'Albert')
    def test_projects_str(self):
        self.assertEqual(str(self.projects),'Some project')