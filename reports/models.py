from django.db import models

from users.models import Department


# Create your models here.
class Reports(models.Model):
    reports_name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    department = models.ManyToManyField('users.Department',blank=True)
    def __str__(self):
        return self.reports_name
    class Meta:
        verbose_name_plural='Reports'