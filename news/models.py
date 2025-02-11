from django.db import models
from users.models import User
from simple_history.models import HistoricalRecords

class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    documents = models.FileField(null=True, blank=True)
    tags = models.ManyToManyField('Tag', related_name='news', blank=True)  # related_name исправлен
    history = HistoricalRecords()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'News'

class NewsComment(models.Model):  # Название модели в единственном числе
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.comment_text

    class Meta:
        verbose_name_plural = 'News Comments'

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
