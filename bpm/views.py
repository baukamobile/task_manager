
from bpm.serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from bpm.bpmn_parser import parse_bpmn_xml_and_save
from rest_framework.response import Response
from rest_framework import status
from par import parse_xml
from bpm.models import BpmnXmlProcess
import xml.etree.ElementTree as ET
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
        serializer.is_valid(raise_exception=True)
        process_instance = serializer.save()
        bpmn_xml_obj = process_instance.bpmn_xml
        xml_str = bpmn_xml_obj.xml
        ns = {
        'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
        'bpmndi': 'http://www.omg.org/spec/BPMN/20100524/DI',
        'di': 'http://www.omg.org/spec/DD/20100524/DI'
        }

        try:
            tree = ET.fromstring(xml_str)
            logger.info(f"Успешно парсено xml строка для этого процесса - {process_instance}")
        except ET.ParseError as e:
            logger.error(f"Ошибка при парсинга xml из процесса - {process_instance}: {e}")
            raise

        element_mapping = {}
        element_order = ['startEvent', 'task', 'parallelGateway','exclusiveGateway', 'endEvent']

        for tag in element_order:
            for elem in tree.findall(f".//bpmn:{tag}", namespaces=ns):
                el_id = elem.attrib['id']
                name = elem.attrib.get('name')
                try:
                    element = ProcessElement.objects.create(
                    process=process_instance,
                    element_id=el_id,
                    element_type=tag,
                    name=name
                )
                    element_mapping[el_id] = element
                    logger.info(f"Создан {tag} элемент: id={el_id}, name={name}")
                except Exception as e:
                    logger.error(f"Ошибка при создании {tag} элемента id={el_id}: {e}")
                    raise
                logger.info(f"Элементы по очередно создан: {list(element_mapping.keys())}")

        for flow in tree.findall(".//bpmn:sequenceFlow", namespaces=ns):
            source_ref = flow.attrib['sourceRef']
            target_ref = flow.attrib['targetRef']

            if source_ref in element_mapping and target_ref in element_mapping:
                try:
                    ProcessLink.objects.create(
                        start_element=element_mapping[source_ref],
                        end_element=element_mapping[target_ref],
                        link_type='sequenceFlow'
                    )
                    logger.info(f"Связи созданы: {source_ref} -> {target_ref}")
                except Exception as e:
                    logger.error(f"Ошибка при создании связи {source_ref} -> {target_ref}: {e}")
                    raise
            else:
                logger.warning(f"Элемент не найден - source_ref={source_ref} или target_ref={target_ref}")

        logger.info(f"Парсинг xml закончен для -  {process_instance}")

    def update(self, request, *args, **kwargs):
        logger.info(f"Received update request: {request.data}")
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        process_instance = serializer.save()

        try:
            bpmn_xml_obj = process_instance.bpmn_xml
            xml_str = bpmn_xml_obj.xml
            ns = {
                'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
                'bpmndi': 'http://www.omg.org/spec/BPMN/20100524/DI',
                'di': 'http://www.omg.org/spec/DD/20100524/DI'
            }

            tree = ET.fromstring(xml_str)
            logger.info(f"Парсинг XML для обновления процесса - {process_instance}")

            # Удалить старые элементы и связи
            ProcessElement.objects.filter(process=process_instance).delete()
            ProcessLink.objects.filter(
                start_element__process=process_instance
            ).delete()

            element_mapping = {}
            element_order = ['startEvent', 'task', 'parallelGateway', 'exclusiveGateway', 'endEvent']

            for tag in element_order:
                for elem in tree.findall(f".//bpmn:{tag}", namespaces=ns):
                    el_id = elem.attrib['id']
                    name = elem.attrib.get('name')
                    element = ProcessElement.objects.create(
                        process=process_instance,
                        element_id=el_id,
                        element_type=tag,
                        name=name
                    )
                    element_mapping[el_id] = element
                    logger.info(f"Обновлён {tag} элемент: id={el_id}, name={name}")

            for flow in tree.findall(".//bpmn:sequenceFlow", namespaces=ns):
                source_ref = flow.attrib['sourceRef']
                target_ref = flow.attrib['targetRef']
                if source_ref in element_mapping and target_ref in element_mapping:
                    ProcessLink.objects.create(
                        start_element=element_mapping[source_ref],
                        end_element=element_mapping[target_ref],
                        link_type='sequenceFlow'
                    )
                    logger.info(f"Обновлён линк: {source_ref} -> {target_ref}")
                else:
                    logger.warning(f"Hе найден элемент — {source_ref} или {target_ref}")

        except Exception as e:
            logger.error(f"Обновление XML сломалось: {e}")
            return Response({"error": str(e)}, status=400)

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


