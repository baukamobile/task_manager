
from bpm.serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from bpm.bpmn_parser import parse_bpmn_xml_and_save
from rest_framework.response import Response
# Create your views here.
class ProcessViewSet(ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        process = serializer.save()
        parse_bpmn_xml_and_save(process)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        process = serializer.save()
        parse_bpmn_xml_and_save(process)
        return Response(serializer.data)
class BpmXmlProcessViewSet(ModelViewSet):
    queryset = BpmnXmlProcess.objects.all()
    serializer_class = BpmnXmlProcessSerializer
    @csrf_exempt
    def create(self, request, *args, **kwargs):
        xml = request.data.get('xml')
        instance = BpmnXmlProcess.objects.create(xml=xml)

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
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


