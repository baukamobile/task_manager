from django.contrib import admin
from bpm.models import *
# Register your models here.
# admin.site.register(Process)
# admin.site.register(WorkflowStep)




# class WorkflowStepAdmin(admin.ModelAdmin):
#     list_display = ('id', 'process', 'name', 'order','requires_approval','responsible_position')
#     list_filter = ('process', 'order','requires_approval')
#     search_fields = ('name', 'process__name')
# admin.site.register(WorkflowStep,WorkflowStepAdmin)

class ProcessAdmin(admin.ModelAdmin):
    list_display = ('name','id',  'created_at')
    list_filter = ( 'created_at',)
    search_fields = ('name',)
admin.site.register(Process, ProcessAdmin)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('process', 'assigned_to','status', 'due_date', 'created_at', 'updated_at','id')
    list_filter = ('process','assigned_to','created_at','due_date','updated_at')
admin.site.register(Task,TaskAdmin)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'filename', 'file', 'uploaded_by','uploaded_at','id')
    list_filter = ('task','uploaded_by','uploaded_at')
admin.site.register(Attachment,AttachmentAdmin)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'text', 'created_at', 'updated_at','id')
    list_filter = ('task', 'author', 'created_at', 'updated_at')
admin.site.register(Comment,CommentAdmin)
class NotificationAdmin(admin.ModelAdmin):
    list_filter = ('user','type','created_at','is_read','id')
    list_display = ('id', 'user', 'task', 'type','message', 'created_at', 'is_read')
admin.site.register(Notification,NotificationAdmin)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'owner', 'is_public')
    list_filter = ('department', 'owner', 'is_public')
admin.site.register(Dashboard,DashboardAdmin)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'dashboard', 'title', 'widget_type', 'department', 'position_x', 'position_y', 'width', 'height')
    list_filter = ('dashboard', 'department', 'widget_type')
admin.site.register(DashboardWidget,DashboardWidgetAdmin)
class BpmnXmlProcessAdmin(admin.ModelAdmin):
    list_display = ('id',)
admin.site.register(BpmnXmlProcess,BpmnXmlProcessAdmin)
class ProcessLinkAdmin(admin.ModelAdmin):
    list_display = ('link_type','start_element','end_element','created_at','id')
admin.site.register(ProcessLink,ProcessLinkAdmin)





# class ProcessTemplateAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'description', 'department', 'created_by', 'created_at')
#     list_filter = ('department', 'created_by', 'created_at')
# admin.site.register(ProcessTemplate,ProcessTemplateAdmin)
# class ProcessStageTemplateAdmin(admin.ModelAdmin):
#     list_display = ('id', 'template', 'name', 'description', 'order', 'is_required', 'completion_criteria','sla_hours')
#     list_filter = ('template', 'order', 'is_required')
#     search_fields = ('template__name', 'name')
# admin.site.register(ProcessStageTemplate,ProcessStageTemplateAdmin)
# class ProcessStageAdmin(admin.ModelAdmin):
#     list_display = ('id','process','template_stage','name','description','order','is_required','completion_criteria','sla_hours','is_custom')
#     list_filter = ('id','process','template_stage','name','description','order','is_required','completion_criteria','sla_hours','is_custom')
# admin.site.register(ProcessStage,ProcessStageAdmin)
# class TaskStageHistoryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'task', 'from_stage', 'to_stage', 'changed_by', 'changed_at', 'comments')
#     list_filter = ('task', 'from_stage', 'to_stage', 'changed_by', 'changed_at')
# admin.site.register(TaskStageHistory,TaskStageHistoryAdmin)
# class AutoTaskRuleAdmin(admin.ModelAdmin):
#     list_display = ('id', 'trigger_stage','source_department', 'target_department', 'target_template', 'description', 'is_active')
#     list_filter = ('trigger_stage','source_department', 'target_department', 'target_template', 'is_active')
# admin.site.register(AutoTaskRule,AutoTaskRuleAdmin)
# class UserDepartmentRoleAdmin(admin.ModelAdmin):
#     list_display = ('user','department','role')
#     list_filter = ('user','department','role')
# admin.site.register(UserDepartmentRole,UserDepartmentRoleAdmin)
# class WorkflowRuleAdmin(admin.ModelAdmin):
#     list_display =('id','from_step','to_step','allowed_position')
#     list_filter = ('id','from_step','to_step','allowed_position')
# admin.site.register(WorkflowRule,WorkflowRuleAdmin)
class ProcessElementAdmin(admin.ModelAdmin):
    list_display = ('id','process','element_id','element_type','name','next_element','created_at')
    list_filter = ('id','process','element_id','element_type','name','next_element','created_at')
admin.site.register(ProcessElement,ProcessElementAdmin)

# class ElementConnectionAdmin(admin.ModelAdmin):
#     list_display = ('id','source','target','label','condition')
# admin.site.register(ElementConnection,ElementConnectionAdmin)
# class ProcessExecutionAdmin(admin.ModelAdmin):
#     list_display = ('id','process','started_at','completed_at','current_element','status')
# admin.site.register(ProcessExecution,ProcessExecutionAdmin)

