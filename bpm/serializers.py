from rest_framework import serializers
from bpm.models import *
class BpmnXmlProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = BpmnXmlProcess
        fields = '__all__'
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
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
class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = '__all__'
class DashboardWidgetSerizalizer(serializers.ModelSerializer):
    class Meta:
        model = DashboardWidget
        fields = '__all__'
class ProcessSerializer(serializers.ModelSerializer):
    # bpmn_xml = BpmnXmlProcessSerializer()
    class Meta:
        model = Process
        fields = '__all__'

# class ProcessTemplateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProcessTemplate
#         fields = '__all__'
# class ProcessStageTemplateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProcessStageTemplate
#         fields = '__all__'
# class ProcessStageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProcessStage
#         fields = '__all__'
#
# class TaskStageHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TaskStageHistory
#         fields = '__all__'
# class AutoTaskRuleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AutoTaskRule
#         fields = '__all__'
# class ProcessElementSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProcessElement
#         fields = '__all__'
# class ElementConnectionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ElementConnection
#         fields = '__all__'
# class ProcessExecutionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProcessExecution
#         fields = '__all__'


    # def to_representation(self, instance):
    #     """Чтобы в ответе возвращались вложенные данные"""
    #     data = super().to_representation(instance)
    #     data['bpmn_xml'] = BpmnXmlProcessSerializer(instance.bpmn_xml).data if instance.bpmn_xml else None
    #     return data
















