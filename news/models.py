from django.db import models
from users.models import User
from simple_history.models import HistoricalRecords

class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True,null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='News_images', null=True,blank=True)
    documents = models.FileField(upload_to='news_documents', null=True, blank=True) #можно создать отделный модель пока так
    tags = models.ManyToManyField('Tag', related_name='news',blank=True)  # related_name исправлен
    history = HistoricalRecords()

    def __str__(self):
        return self.title
    def like_count(self):
        return self.likes.count()

    class Meta:
        verbose_name_plural = 'News'
class likes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    news = models.ForeignKey(News,on_delete=models.CASCADE,related_name='likes')
    created_at= models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user','news')
    def __str__(self):
        return f"{self.user} поставил лайк на {self.news}"

# class Congrutulations(models.Model):

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
