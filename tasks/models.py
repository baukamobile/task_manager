from django.db import models
from users.models import User,Department
# import logging
from simple_history.models import HistoricalRecords
# logger = logging.getLogger(__name__)



# ACTIVE= 'АКТИВЕН' IN_PROCESS= 'В ПРОЦЕССЕ' COMPLETED= 'ЗАКОНЧЕН'NON_ACTIVE='НЕ АКТИВЕН'TO_DELETE = 'К УДАЛЕНИЮ'STATUS_CHOICES = [(ACTIVE, 'АКТИВЕН'),(IN_PROCESS, 'В ПРОЦЕССЕ'),(COMPLETED, 'ЗАКОНЧЕН'),(NON_ACTIVE,'НЕ АКТИВЕН'),(TO_DELETE,'К УДАЛЕНИЮ')]
# TECHNICAL_DEBT = 'ТЕХНИЧЕСКИЙ ДОЛГ'LOW='НИЗКИЙ'MEDIUM = 'СРЕДНИЙ'HIGH='ВЫСОКИЙ'CRITICAL='КРИТИЧЕСКИЙ'

# PRIORITY_CHOISES = [(LOW,'НИЗКИЙ'),(MEDIUM, 'СРЕДНИЙ'),(HIGH,'ВЫСОКИЙ'),(CRITICAL,'КРИТИЧЕСКИЙ'),(TECHNICAL_DEBT,'ТЕХНИЧЕСКИЙ ДОЛГ')]


class Task(models.Model):
    task_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    documents = models.FileField(upload_to='task_documents', null=True, blank=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='tasks')  # Теперь только через статус
    assigned = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    priority = models.ForeignKey('Priority', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    agreed_with_managers = models.BooleanField(default=False)
    department = models.ForeignKey('users.Department', on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        # logger.debug('shows task_name {}'.format(self.task_name))
        return self.task_name

    class Meta:
        verbose_name_plural='Task'
        ordering = ['-start_date']
        #количество коментариев внутри задач
    def comments_count(self):
        return self.comments.count()




class Status(models.Model):
    status_name = models.CharField(max_length=100)
    # user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='statususers')
    project = models.ForeignKey('Projects', on_delete=models.CASCADE,
                                related_name='statuses',null=True,blank=True)  # связь со статусами проекта

    def __str__(self):
        return self.status_name
    class Meta:
        verbose_name_plural='Status'


class Priority(models.Model):
    priority_name = models.CharField(max_length=100)
    # user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='priorityusers')
    # project = models.ForeignKey('Projects', on_delete=models.CASCADE, related_name='statuses')
    def __str__(self):
        return self.priority_name
    class Meta:
        verbose_name_plural='Priority'

class Projects(models.Model): #название проекта
    project_name = models.CharField(max_length=100,db_index=True)
    description = models.TextField(null=True,blank=True)
    department = models.ForeignKey('users.Department', on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    assigned = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,db_index=True)
    end_date = models.DateTimeField()
    history = HistoricalRecords()

    @property
    def tasks(self):
        return Task.objects.filter(status__in=self.statuses.all())

    def __str__(self):
        return self.project_name
    class Meta:
        verbose_name_plural='Projects'

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
