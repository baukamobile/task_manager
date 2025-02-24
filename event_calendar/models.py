from django.db import models

from users.models import User
from simple_history.models import HistoricalRecords

# Create your models here.
class Event(models.Model):
    BIRTHDAY = 'ДЕНЬ РОЖДЕНИЕ'
    EVENT = 'МЕРОПРИЯТИЕ'
    ACHIEVEMENT = 'ДОСТИЖЕНИЕ'
    AWARD = 'НАГРАДА'
    EVENT_TYPES = [
        (BIRTHDAY, 'ДЕНЬ РОЖДЕНИЕ'),
        (EVENT, 'МЕРОПРИЯТИЕ'),
        (ACHIEVEMENT, 'ДОСТИЖЕНИЕ'),
        (AWARD,'НАГРАДА')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=100,choices=EVENT_TYPES,null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(blank=True,null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'Имя пользователя: {self.user_id} Тип мерориятии: {self.event_type}'
