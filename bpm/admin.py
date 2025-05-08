from django.contrib import admin
from bpm.models import *

class ProcessAdmin(admin.ModelAdmin):
    list_display = ('name','id',  'created_at')
    list_filter = ( 'created_at',)
    search_fields = ('name',)
admin.site.register(Process, ProcessAdmin)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('process', 'assigned_to','status','element', 'due_date','return_reason', 'created_at','completed_at','bpmn_task_id','id')
    list_filter = ('process', 'assigned_to','status', 'due_date','return_reason', 'created_at', 'updated_at','completed_at','id')
admin.site.register(Task,TaskAdmin)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'filename', 'file', 'uploaded_by','uploaded_at','id')
    list_filter = ('task','uploaded_by','uploaded_at')
admin.site.register(Attachment,AttachmentAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_filter = ('user','type','created_at','is_read','id')
    list_display = ('id', 'user', 'task', 'type','message', 'created_at', 'is_read')
admin.site.register(Notification,NotificationAdmin)

class BpmnXmlProcessAdmin(admin.ModelAdmin):
    list_display = ('id',)
admin.site.register(BpmnXmlProcess,BpmnXmlProcessAdmin)
class ProcessLinkAdmin(admin.ModelAdmin):
    list_display = ('process','link_type','start_element','end_element','source_type','target_type','created_at','id')
admin.site.register(ProcessLink,ProcessLinkAdmin)
class ProcessElementAdmin(admin.ModelAdmin):
    list_display = ('process','element_id','element_type','name','assigned','annotation','created_at','id',)
    list_filter = ('id','process','element_id','element_type','name','created_at')
admin.site.register(ProcessElement,ProcessElementAdmin)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('process','element','status','parent_token','created_at')
    list_filter = ('process','element','status','parent_token','created_at')
admin.site.register(Token,TokenAdmin)
class GatewayConditionAdmin(admin.ModelAdmin):
    list_display = ('process','element','condition_type','condition_value','target_element')
    list_filter = ('process', 'element', 'condition_type', 'condition_value', 'target_element')
admin.site.register(GatewayCondition,GatewayConditionAdmin)