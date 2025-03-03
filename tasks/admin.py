from django.contrib import admin
from tasks.models import *
# Register your models here.
from users.admin import GetEmployeesMixin

class GetCommentMixin:
    def get_comments(self, obj):
        comments = [task.comment for task in obj.comments.all()]  # обявляем переменную коментарий задаем длину

        return ', '.join(comment[:20] + '...' if len(comment) > 10 else comment for comment in comments)
    def get_tasks_name(self,obj):
        task_name= [task.task_name for task in obj.tasks.all()]
        return ', '.join(comment[:8]+ '...' if len(comment) > 10 else comment for comment in task_name)



class TaskAdmin(admin.ModelAdmin, GetCommentMixin):
    change_list_template = "tasks/task.html"
    list_display = ['task_name', 'assigned', 'start_date', 'end_date', 'get_comments', 'agreed_with_managers']

    def changelist_view(self, request, extra_context=None):
        task_statuses = Status.objects.all()
        labels = []
        values = []
        for status in task_statuses:
            labels.append(status.status_name)  # или другой атрибут, который хранит название статуса
            count = Task.objects.filter(status=status).count()
            values.append(count)

        if extra_context is None:
            extra_context = {}
        extra_context['labels'] = labels
        extra_context['values'] = values

        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(Task,TaskAdmin)

class StatusAdmin(admin.ModelAdmin):
    list_filter = ['id']
    list_display = ['id','status_name']
admin.site.register(Status,StatusAdmin)


class PriorityAdmin(admin.ModelAdmin):
    list_display = ['id','priority_name']
admin.site.register(Priority,PriorityAdmin)




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