from django.db import models

from users.models import Department
from event_calendar.models import Event
from users.models import User
from django.core.exceptions import ValidationError



# Create your models here.
class Reports(models.Model):
    reports_name = models.CharField(max_length=100)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    department = models.ManyToManyField('users.Department',blank=True,related_name='reports')
    # event_report = models.ManyToManyField(Event.EVENT_TYPES,null=True,blank=True)
    employees_report = models.ManyToManyField(User,blank=True,related_name='employees_report')
    def __str__(self):
        return self.reports_name

    def clean(self):
        if self.start_date and self.end_date and self.start_date >= self.end_date: #
            raise ValidationError('Дата окончание не должно быть раьше чем дата начало')
    class Meta:
        verbose_name_plural='Reports'