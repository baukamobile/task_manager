from django.db import models
from users.models import User,Department
# import logging
from simple_history.models import HistoricalRecords
# logger = logging.getLogger(__name__)

# Create your models here.
class Task(models.Model):
    ACTIVE= 'АКТИВЕН'
    IN_PROCESS= 'В ПРОЦЕССЕ'
    COMPLETED= 'ЗАКОНЧЕН'
    NON_ACTIVE='НЕ АКТИВЕН'
    TO_DELETE = 'К УДАЛЕНИЮ'
    STATUS_CHOICES = [(ACTIVE, 'АКТИВЕН'),(IN_PROCESS, 'В ПРОЦЕССЕ'),(COMPLETED, 'ЗАКОНЧЕН'),(NON_ACTIVE,'НЕ АКТИВЕН'),(TO_DELETE,'К УДАЛЕНИЮ')]
    TECHNICAL_DEBT = 'ТЕХНИЧЕСКИЙ ДОЛГ'
    LOW='НИЗКИЙ'
    MEDIUM = 'СРЕДНИЙ'
    HIGH='ВЫСОКИЙ'
    CRITICAL='КРИТИЧЕСКИЙ'

    PRIORITY_CHOISES = [
        (LOW,'НИЗКИЙ'),
        (MEDIUM, 'СРЕДНИЙ'),
        (HIGH,'ВЫСОКИЙ'),
        (CRITICAL,'КРИТИЧЕСКИЙ'),
        (TECHNICAL_DEBT,'ТЕХНИЧЕСКИЙ ДОЛГ')
    ]
    task_name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    tags = models.TextField(blank=True, null=True)
    # files = models.ForeignKey(Files, on_delete=models.SET_NULL, null=True,blank=True)
    documents = models.FileField(null=True, blank=True)
    projects = models.ForeignKey('Projects',default=1,on_delete=models.SET_DEFAULT, blank=True, related_name='tasks')
    assigned = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,db_index=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=100, default=ACTIVE,db_index=True)
    priority = models.CharField(choices=PRIORITY_CHOISES, max_length=100)
    department = models.ForeignKey('users.Department', on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        # logger.debug('shows task_name {}'.format(self.task_name))
        return self.task_name
    class Meta:
        verbose_name_plural='Task'
        ordering = ['-start_date']


class Projects(models.Model): #название проекта
    project_name = models.CharField(max_length=100,db_index=True)
    description = models.TextField(null=True,blank=True)
    department = models.ForeignKey('users.Department', on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    history = HistoricalRecords()

    def __str__(self):
        return self.project_name
    class Meta:
        verbose_name_plural='Projects'

class Task_comments(models.Model):
    task = models.ForeignKey(Task, on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    comment = models.TextField()
    documents = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField()
    history = HistoricalRecords()

    def __str__(self):
        return self.comment
    class Meta:
        verbose_name_plural='Task Comments'
