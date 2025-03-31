from django.test import TestCase
from bpm.models import Process, Department
from django.contrib.auth import get_user_model

User = get_user_model()

class ProcessTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name='Albert',
            email='albert@gmail.com',
            phone_number=1874658,
            password='sdfsdjfjsd34'
        )
        self.department = Department.objects.create(
            department_name='soem dep',
            department_head=self.user
        )
        self.process = Process.objects.create(
            name="Test Process",
            department=self.department,
            created_by=self.user
        )

    def test_process_creation(self):
        process = Process.objects.get(id=self.process.id)
        self.assertEqual(process.department, self.department)
        self.assertEqual(process.created_by, self.user)

        # task = Task.objects.get(id=self.task.id)
        # self.assertEqual(task.task_name, "Task Name")
        # class Process(models.Model):
        #     name = models.CharField(max_length=100)
        #     department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='process', null=True,
        #                                    blank=True)
        #     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_process', null=True,
        #                                    blank=True)
        #     created_at = models.DateTimeField(null=True, blank=True)
        #     end_date = models.DateTimeField(null=True, blank=True)
        #
        #     def __str__(self):
        #         return self.name
        #
        # class WorkflowStep(models.Model):  # Этапы
        #     process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='steps')
        #     name = models.CharField(max_length=255)
        #     order = models.PositiveIntegerField()  # Определяет порядок этапов
        #     requires_approval = models.BooleanField(default=False)  # Нужен ли ручной контроль
        #
        #     def __str__(self):
        #         return f"{self.process.name} - {self.name}"