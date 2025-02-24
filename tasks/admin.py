from django.contrib import admin
from tasks.models import *
# Register your models here.
from users.admin import GetEmployeesMixin

class GetCommentMixin:
    def get_comments(self, obj):
        comments = [task.comment for task in obj.comments.all()]  # обявляем переменную коментарий задаем длину
        #Склеиваем их в строку, обрезая те, которые длиннее 10 символов

        return ', '.join(comment[:20] + '...' if len(comment) > 10 else comment for comment in comments)




class TaskAdmin(admin.ModelAdmin,GetCommentMixin):
    list_display = ['task_name','assigned','projects','start_date','end_date','get_comments']


admin.site.register(Task,TaskAdmin)



class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'user', 'short_comment', 'created_at']
    def short_comment(self, obj): #функция сокращает длину комменарий
        return obj.comment[:10] + '...' if len(obj.comment) > 10 else obj.comment

    short_comment.short_description = "Comment"

admin.site.register(Task_comments,TaskCommentAdmin)

admin.site.register(Projects)