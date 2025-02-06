from django.db import models
from users.models import User
# Create your models here.
class News(models.Model):

    title = models.CharField(max_length=100)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class News_comments(models.Model):
    news_id = models.ForeignKey(News, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_text