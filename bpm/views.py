from idlelib.multicall import MC_DESTROY

from django.shortcuts import render
from bpm.models import *
from bpm.serializers import (ProcessSerializer, ProcessTemplateSerializer, ProcessStageSerializer, TaskSerializer,
                             TaskStageHistorySerializer, ProcessStageTemplateSerializer, AutoTaskRuleSerializer,
                             AttachmentSerializer,
                             CommentSerializer, NotificationSerializer, DashboardSerializer, DashboardWidgetSerizalizer,
                             ProcessElementSerializer, ElementConnectionSerializer, ProcessExecutionSerializer,
                             BpmnXmlProcessSerializer
                             )
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
# Create your views here.
class ProcessViewSet(ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer

# class WorkflowStepViewSet(ModelViewSet):
#     queryset = WorkflowStep.objects.all()
#     serializer_class = WorkflowStepSerializer

class ProcessTemplateViewSet(ModelViewSet):
    queryset = ProcessTemplate.objects.all()
    serializer_class = ProcessTemplateSerializer
class ProcessStageTemplateViewSet(ModelViewSet):
    queryset = ProcessStageTemplate.objects.all()
    serializer_class = ProcessStageTemplateSerializer
class ProcessStageViewSet(ModelViewSet):
    queryset = ProcessStage.objects.all()
    serializer_class = ProcessStageSerializer
class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
class TaskStageHistoryViewSet(ModelViewSet):
    queryset = TaskStageHistory.objects.all()
    serializer_class = TaskStageHistorySerializer
class AutoTaskRuleViewSet(ModelViewSet):
    queryset = AutoTaskRule.objects.all()
    serializer_class = AutoTaskRuleSerializer
class AttachmentViewSet(ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
# class UserDepartmentRoleViewSet(ModelViewSet):
#     queryset = UserDepartmentRole.objects.all()
#     serializer_class = UserDepartmentRoleSerializer
class DashboardWidgetViewSet(ModelViewSet):
    queryset = DashboardWidget.objects.all()
    serializer_class = DashboardWidgetSerizalizer
class DashboardViewSet(ModelViewSet):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer

class ProcessElementViewSet(ModelViewSet):
    queryset = ProcessElement.objects.all()
    serializer_class = ProcessElementSerializer
class ElementConnectionViewSet(ModelViewSet):
    queryset = ElementConnection.objects.all()
    serializer_class = ElementConnectionSerializer
    serializer_class = ElementConnectionSerializer
class ProcessExecutionViewSet(ModelViewSet):
    queryset = ProcessExecution.objects.all()
    serializer_class = ProcessExecutionSerializer

class BpmXmlProcessViewSet(ModelViewSet):
    queryset = BpmnXmlProcess.objects.all()
    serializer_class = BpmnXmlProcessSerializer
    @csrf_exempt
    def create(self, request, *args, **kwargs):
        xml = request.data.get('xml')
        instance = BpmnXmlProcess.objects.create(xml=xml)
        return Response({'status': 'ok', 'id': instance.id}, status=status.HTTP_201_CREATED)
