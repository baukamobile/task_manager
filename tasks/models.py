from contextlib import nullcontext
from email.policy import default

from django.db import models
from users.models import User,Department
# import logging
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
# logger = logging.getLogger(__name__)



# ACTIVE= 'АКТИВЕН' IN_PROCESS= 'В ПРОЦЕССЕ' COMPLETED= 'ЗАКОНЧЕН'NON_ACTIVE='НЕ АКТИВЕН'TO_DELETE = 'К УДАЛЕНИЮ'STATUS_CHOICES = [(ACTIVE, 'АКТИВЕН'),(IN_PROCESS, 'В ПРОЦЕССЕ'),(COMPLETED, 'ЗАКОНЧЕН'),(NON_ACTIVE,'НЕ АКТИВЕН'),(TO_DELETE,'К УДАЛЕНИЮ')]
# TECHNICAL_DEBT = 'ТЕХНИЧЕСКИЙ ДОЛГ'LOW='НИЗКИЙ'MEDIUM = 'СРЕДНИЙ'HIGH='ВЫСОКИЙ'CRITICAL='КРИТИЧЕСКИЙ'




class Task(models.Model):
    task_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    documents = models.FileField(upload_to='task_documents', null=True, blank=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='tasks',default=1)
    assigned = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    priority = models.ForeignKey('Priority', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    agreed_with_managers = models.BooleanField(default=False)
    project = models.ForeignKey('Projects', on_delete=models.CASCADE, related_name='tasks',default=1)
    department = models.ForeignKey('users.Department', on_delete=models.CASCADE, related_name='tasks')
    history = HistoricalRecords()

    def __str__(self):
        return self.task_name

    def clean(self):
        if self.status.project != self.project:
            raise ValidationError('Статус не принадлежит выбранному проекту.')

    def comments_count(self):
        return self.comments.count()

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-start_date']


class Status(models.Model):
    status_name = models.CharField(max_length=100)
    project = models.ForeignKey('Projects', on_delete=models.CASCADE, related_name='statuses',default=1)

    def __str__(self):
        return self.status_name

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'


class Priority(models.Model):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    CRITICAL = 'CRITICAL'
    TECHNICAL_DEBT = 'TECHNICAL_DEBT'
    PRIORITY_CHOICES = [
        (LOW, 'НИЗКИЙ'), (MEDIUM, 'СРЕДНИЙ'), (HIGH, 'ВЫСОКИЙ'),
        (CRITICAL, 'КРИТИЧЕСКИЙ'), (TECHNICAL_DEBT, 'ТЕХНИЧЕСКИЙ ДОЛГ')
    ]
    priority_name = models.CharField(max_length=30, choices=PRIORITY_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.priority_name or '-'

    class Meta:
        verbose_name = 'Priority'
        verbose_name_plural = 'Priorities'


class Projects(models.Model):
    project_name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=True, blank=True)
    department = models.ForeignKey('users.Department', on_delete=models.CASCADE, related_name='projects')
    start_date = models.DateTimeField(auto_now_add=True)
    assigned = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
    end_date = models.DateTimeField()
    history = HistoricalRecords()

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'


class Task_comments(models.Model):
    task = models.ForeignKey(Task, on_delete=models.SET_NULL,null=True,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    comment = models.TextField()
    documents = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.comment
    class Meta:
        verbose_name_plural='Task Comments'
