from django.db import models
from simple_history.models import HistoricalRecords
from users.models import User
# Create your models here.

class Chat(models.Model):
    chat_name = models.CharField(max_length=100)
    chat_type = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)  #user_id
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chat_name


class Messages(models.Model):
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE)  # foreign key user id
    message_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # sent_by = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    sent_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.message_text

class MessageHistory(models.Model):
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE)  # foreign key from user id
    message_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.message_text
