from django.db import models
from users.models import Department,User
# Create your models here.
class Process(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,related_name='process',null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='created_process',null=True,blank=True)
    created_at = models.DateTimeField(null=True,blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
class WorkflowStep(models.Model): #Этапы
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='steps')
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField()  # Определяет порядок этапов
    requires_approval = models.BooleanField(default=False)  # Нужен ли ручной контроль

    def __str__(self):
        return f"{self.process.name} - {self.name}"