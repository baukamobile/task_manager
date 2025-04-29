
from bpm.serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from bpm.bpmn_parser import parse_bpmn_xml_and_save
from rest_framework.response import Response
from rest_framework import status
from par import parse_xml
from bpm.models import BpmnXmlProcess
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Process, BpmnXmlProcess, ProcessElement, ProcessLink
from .serializers import ProcessSerializer
import logging
import xml.etree.ElementTree as ET

logger = logging.getLogger('bpm')

class ProcessViewSet(ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        logger.info(f"Received create request: {request.data}")
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        process = serializer.save()

        try:
            bpmn_xml_obj = BpmnXmlProcess.objects.get(id=process.bpmn_xml)
            xml_str = bpmn_xml_obj.xml
            logger.info(f"Parsed XML string: {repr(xml_str[:200])}")

            self.parse_xml(xml_str, process)
            logger.info(f"Successfully parsed BPMN XML for process {process.id}")

        except Exception as e:
            logger.error(f"Failed to parse BPMN XML for process {process.id}: {e}")
            return Response({"error": f"Failed to parse BPMN XML: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        logger.info(f"Received update request: {request.data}")
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        process = serializer.save()

        try:
            # Получаем XML данные из запроса
            xml_str = request.data.get('xml') or request.data.get('bpmn_xml')
            logger.info(f"XML string raw: {type(xml_str)} - {repr(str(xml_str)[:200])}")

            if xml_str:
                # Если это файл
                if hasattr(xml_str, 'read'):
                    xml_str = xml_str.read().decode('utf-8')
                # Парсим XML и обновляем элементы
                self.parse_xml(xml_str, process)
                logger.info(f"Successfully updated BPMN XML for process {process.id}")
            else:
                logger.info(f"No XML provided for process {process.id}")

        except Exception as e:
            logger.error(f"Failed to update BPMN XML for process {process.id}: {e}")
            return Response({"error": f"Failed to parse BPMN XML: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

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


