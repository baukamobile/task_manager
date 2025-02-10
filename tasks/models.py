from django.db import models
from users.models import User,Department
import logging
from simple_history.models import HistoricalRecords

logger = logging.getLogger(__name__)

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
    tags = models.TextField(blank=True, null=True)
    projects = models.ManyToManyField('Projects', blank=True)
    assigned = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,db_index=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=100, default=ACTIVE,db_index=True)
    priority = models.CharField(choices=PRIORITY_CHOISES, max_length=100)
    department = models.ForeignKey('users.Department', on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        logger.debug('shows task_name {}'.format(self.task_name))
        return self.task_name


class Projects(models.Model):
    project_name = models.CharField(max_length=100,db_index=True)
    description = models.TextField()
    department = models.ForeignKey('users.Department', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    history = HistoricalRecords()

    def __str__(self):
        return self.project_name

class Task_comments(models.Model):
    task = models.ForeignKey(Task, on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    comment = models.TextField()
    created_at = models.DateTimeField()
    history = HistoricalRecords()

    def __str__(self):
        return self.comment
