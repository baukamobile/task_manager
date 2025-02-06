from django.contrib import admin
from tasks.models import *
# Register your models here.

admin.site.register(Task)
# admin.site.register(Departments)
admin.site.register(taskcomments)
admin.site.register(Projects)