from django.db import models
from users.models import User
# Create your models here.
class Notification(models.Model):
    BIRTHDAY = 'ДЕНЬ РОЖДЕНИЕ'
    EVENT = 'МЕРОПРИЯТИЕ'
    ACHIEVEMENT = 'ДОСТИЖЕНИЕ'
    AWARD = 'НАГРАДА'
    NOTIFICATION_TYPES = [
        (BIRTHDAY, 'ДЕНЬ РОЖДЕНИЕ'),
        (EVENT, 'МЕРОПРИЯТИЕ'),
        (ACHIEVEMENT, 'ДОСТИЖЕНИЕ'),
        (AWARD, 'НАГРАДА')

    ]
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_text = models.TextField()
    notification_type = models.CharField(max_length=100, choices=NOTIFICATION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return self.notification_type
    class Meta:
        ordering = ['-created_at']

