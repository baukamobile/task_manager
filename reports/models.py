from django.db import models

from users.models import Department


# Create your models here.
class Reports(models.Model):
    reports_name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    department_id = models.ForeignKey('users.Department', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.reports_name