from django.contrib import admin
from tasks.models import *
# Register your models here.
from users.admin import GetEmployeesMixin

class GetCommentMixin:
    def get_comments(self, obj):
        comments = [task.comment for task in obj.comments.all()]  # обявляем переменную коментарий задаем длину
        #Склеиваем их в строку, обрезая те, которые длиннее 10 символов

        return ', '.join(comment[:20] + '...' if len(comment) > 10 else comment for comment in comments)
    def get_tasks_name(self,obj):
        task_name= [task.task_name for task in obj.tasks.all()]
        # return task_name
        return ', '.join(comment[:8]+ '...' if len(comment) > 10 else comment for comment in task_name)



class TaskAdmin(admin.ModelAdmin,GetCommentMixin):
    list_display = ['task_name','assigned','projects','start_date','end_date','get_comments','agreed_with_managers']
    # list_filter = ['task_name','status','priority','agreed_with_managers']

admin.site.register(Task,TaskAdmin)

class StatusAdmin(admin.ModelAdmin):
    list_filter = ['id']
    list_display = ['id','status_name']
admin.site.register(Status,StatusAdmin)
admin.site.register(Priority)




class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'user', 'short_comment', 'created_at']
    def short_comment(self, obj): #функция сокращает длину комменарий
        return obj.comment[:10] + '...' if len(obj.comment) > 10 else obj.comment

    short_comment.short_description = "Comment"

admin.site.register(Task_comments,TaskCommentAdmin)

class ProjectAdmin(GetCommentMixin,admin.ModelAdmin):
    list_display = ['project_name','get_tasks_name','department','start_date','assigned','end_date']
    list_filter = ['department']


admin.site.register(Projects,ProjectAdmin)