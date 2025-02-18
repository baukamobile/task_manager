from django.contrib import admin
from tasks.models import *
# Register your models here.
from users.admin import GetEmployeesMixin


class TaskAdmin(admin.ModelAdmin):
    list_display = ['task_name','tags','projects','start_date','end_date']
admin.site.register(Task,TaskAdmin)

# admin.site.register(Departments)

class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'user', 'short_comment', 'created_at']
    def short_comment(self, obj):
        return obj.comment[:10] + '...' if len(obj.comment) > 10 else obj.comment

    short_comment.short_description = "Comment"

admin.site.register(Task_comments,TaskCommentAdmin)

admin.site.register(Projects)