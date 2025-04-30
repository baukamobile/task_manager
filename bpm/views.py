from rest_framework.views import APIView

from bpm.serializers import *
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from par import parse_xml
from bpm.models import BpmnXmlProcess
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Process, BpmnXmlProcess, ProcessElement, ProcessLink
from .serializers import ProcessSerializer
import logging

logger = logging.getLogger('bpm')

class BpmXmlProcessViewSet(ModelViewSet):
    queryset = BpmnXmlProcess.objects.all()
    logger.info('bpmn xml processviewset')
    serializer_class = BpmnXmlProcessSerializer
    @csrf_exempt
    def create(self, request, *args, **kwargs):
        xml = request.data.get('xml')
        instance = BpmnXmlProcess.objects.create(xml=xml)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    logger.info("Task viewset")
    serializer_class = TaskSerializer

class AttachmentViewSet(ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
class DashboardWidgetViewSet(ModelViewSet):
    queryset = DashboardWidget.objects.all()
    serializer_class = DashboardWidgetSerizalizer
class DashboardViewSet(ModelViewSet):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
class ProcessElementViewSet(ModelViewSet):
    queryset = ProcessElement.objects.all()
    serializer_class = ProcessElementSerializer


#         return Response({'status': 'ok', 'id': instance.id}, status=status.HTTP_201_CREATED)
# class ProcessTemplateViewSet(ModelViewSet):
#     queryset = ProcessTemplate.objects.all()
#     serializer_class = ProcessTemplateSerializer
# class ProcessStageTemplateViewSet(ModelViewSet):
#     queryset = ProcessStageTemplate.objects.all()
#     serializer_class = ProcessStageTemplateSerializer
# class ProcessStageViewSet(ModelViewSet):
#     queryset = ProcessStage.objects.all()
#     serializer_class = ProcessStageSerializer
# class TaskStageHistoryViewSet(ModelViewSet):
#     queryset = TaskStageHistory.objects.all()
#     serializer_class = TaskStageHistorySerializer
# class AutoTaskRuleViewSet(ModelViewSet):
#     queryset = AutoTaskRule.objects.all()
#     serializer_class = AutoTaskRuleSerializer
#
# # class UserDepartmentRoleViewSet(ModelViewSet):
# #     queryset = UserDepartmentRole.objects.all()
# #     serializer_class = UserDepartmentRoleSerializer
#
#

# class ElementConnectionViewSet(ModelViewSet):
#     queryset = ElementConnection.objects.all()
#     serializer_class = ElementConnectionSerializer
#     # serializer_class = ElementConnectionSerializer
# class ProcessExecutionViewSet(ModelViewSet):
#     queryset = ProcessExecution.objects.all()
#     serializer_class = ProcessExecutionSerializer


