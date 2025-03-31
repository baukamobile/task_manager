from django.contrib import admin
from bpm.models import *
# Register your models here.
# admin.site.register(Process)
admin.site.register(WorkflowStep)
admin.site.register(ProcessTemplate)
admin.site.register(ProcessStageTemplate)
admin.site.register(Process)
admin.site.register(ProcessStage)
admin.site.register(Task)
admin.site.register(TaskStageHistory)
admin.site.register(AutoTaskRule)
admin.site.register(Attachment)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(UserDepartmentRole)
admin.site.register(Dashboard)
admin.site.register(DashboardWidget)
