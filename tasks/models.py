from django.db import models
from users.models import User,Department

# Create your models here.
class Task(models.Model):
    ACTIVE= 'АКТИВЕН'
    IN_PROCESS= 'В ПРОЦЕССЕ'
    COMPLETED= 'ЗАКОНЧЕН'

    STATUS_CHOICES = [
        (ACTIVE, 'АКТИВЕН'),
        (IN_PROCESS, 'В ПРОЦЕССЕ'),
        (COMPLETED, 'ЗАКОНЧЕН')
    ]
    Technical_Debt = 'Tехнический долг'
    Low='Низкий'
    Medium = 'Средний'
    High='Высокий'
    Critical='Критический'
    PRIORITY_CHOISES = [
        ( Low,'Низкий'),
        (Medium, 'Средний'),
        (High,'Высокий'),
        (Critical,'Критический'),
        (Technical_Debt,'Tехнический долг')
    ]
    task_name = models.CharField(max_length=100)
    description = models.TextField()
    project_id = models.ForeignKey('Projects', on_delete=models.SET_NULL, null=True, blank=True)
    asigned_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=100, default=ACTIVE)
    priority = models.CharField(choices=PRIORITY_CHOISES, max_length=100)
    department = models.ForeignKey('users.Department', on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name


class Projects(models.Model):
    project_name = models.CharField(max_length=100)
    description = models.TextField()
    departement = models.ForeignKey('users.Department', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.project_name


# class Departments(models.Model):
#     department_name = models.CharField(max_length=100)
#     department_head = models.CharField(max_length=100)

class taskcomments(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE,null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    comment = models.TextField()
    created_at = models.DateTimeField()
    def __str__(self):
        return self.comment
