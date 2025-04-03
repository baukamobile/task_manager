from rest_framework import serializers
from bpm.models import (Process,WorkflowStep,ProcessTemplate,ProcessStageTemplate,ProcessStage,
                        Task,TaskStageHistory,AutoTaskRule,Attachment,
                        Comment,Notification,UserDepartmentRole,Dashboard,DashboardWidget)

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = '__all__'
class WorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowStep
        fields = '__all__'

class ProcessTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessTemplate
        fields = '__all__'
class ProcessStageTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessStageTemplate
        fields = '__all__'
class ProcessStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessStage
        fields = '__all__'
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
class TaskStageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStageHistory
        fields = '__all__'
class AutoTaskRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoTaskRule
        fields = '__all__'
class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
class UserDepartmentRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDepartmentRole
        fields = '__all__'
class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = '__all__'
class DashboardWidgetSerizalizer(serializers.ModelSerializer):
    class Meta:
        model = DashboardWidget
        fields = '__all__'
