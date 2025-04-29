from rest_framework.views import APIView

from bpm.serializers import *
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from par import parse_xml
from bpm.models import BpmnXmlProcess
import xml.etree.ElementTree as ET

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
        self._parse_and_sync_xml(process_instance)
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        logger.info(f"Received update request: {request.data}")
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        process_instance = serializer.save()
        self._parse_and_sync_xml(process_instance)
        return Response(serializer.data)
    def _parse_and_sync_xml(self, process_instance):
        bpmn_xml_obj = process_instance.bpmn_xml
        xml_str = bpmn_xml_obj.xml
        ns = {
            'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
            'bpmndi': 'http://www.omg.org/spec/BPMN/20100524/DI',
            'di': 'http://www.omg.org/spec/DD/20100524/DI'
        }
        try:
            tree = ET.fromstring(xml_str)
            logger.info(f"XML распарсен для процесса: {process_instance}")
        except ET.ParseError as e:
            logger.error(f"Ошибка парсинга XML: {e}")
            raise
        element_mapping = {}
        element_order = ['startEvent', 'task', 'parallelGateway', 'exclusiveGateway', 'endEvent']
        for tag in element_order:
            for elem in tree.findall(f".//bpmn:{tag}", namespaces=ns):
                el_id = elem.attrib['id']
                name = elem.attrib.get('name')
                try:
                    element, _ = ProcessElement.objects.update_or_create(
                        process=process_instance,
                        element_id=el_id,
                        defaults={
                            'element_type': tag,
                            'name': name
                        }
                    )
                    element_mapping[el_id] = element
                    logger.info(f"{'Создан' if _ else 'Обновлён'} элемент: {el_id} - {name}")
                except Exception as e:
                    logger.error(f"Ошибка при сохранении элемента {el_id}: {e}")
                    raise
        # Удаляем старые линки перед созданием новых, иначе будут дубли
        ProcessLink.objects.filter(start_element__process=process_instance).delete()
        for flow in tree.findall(".//bpmn:sequenceFlow", namespaces=ns):
            source_ref = flow.attrib['sourceRef']
            target_ref = flow.attrib['targetRef']
            try:
                if source_ref in element_mapping and target_ref in element_mapping:
                    ProcessLink.objects.create(
                        start_element=element_mapping[source_ref],
                        end_element=element_mapping[target_ref],
                        link_type='sequenceFlow'
                    )
                    logger.info(f"Линк создан: {source_ref} -> {target_ref}")
                else:
                    logger.warning(f"Пропущен линк, не найдены элементы: {source_ref} или {target_ref}")
            except Exception as e:
                logger.error(f"Ошибка при создании линка {source_ref} -> {target_ref}: {e}")
                raise


class ProcessUpdateXmlView(APIView):
    def parse_and_sync_xml(self, process_instance):
        # Get XML string directly
        xml_str = process_instance.bpmn_xml.xml

        ns = {
            'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
            'bpmndi': 'http://www.omg.org/spec/BPMN/20100524/DI',
            'di': 'http://www.omg.org/spec/DD/20100524/DI'
        }
        try:
            tree = ET.fromstring(xml_str)
            logger.info(f"XML распарсен для процесса: {process_instance}")
        except ET.ParseError as e:
            logger.error(f"Ошибка парсинга XML: {e}")
            raise
        element_mapping = {}
        element_order = ['startEvent', 'task', 'parallelGateway', 'exclusiveGateway', 'endEvent']
        for tag in element_order:
            for elem in tree.findall(f".//bpmn:{tag}", namespaces=ns):
                el_id = elem.attrib['id']
                name = elem.attrib.get('name')
                try:
                    element, _ = ProcessElement.objects.update_or_create(
                        process=process_instance,
                        element_id=el_id,
                        defaults={
                            'element_type': tag,
                            'name': name
                        }
                    )
                    element_mapping[el_id] = element
                    logger.info(f"{'Создан' if _ else 'Обновлён'} элемент: {el_id} - {name}")
                except Exception as e:
                    logger.error(f"Ошибка при сохранении элемента {el_id}: {e}")
                    raise
        # Удаляем старые линки перед созданием новых, иначе будут дубли
        ProcessLink.objects.filter(start_element__process=process_instance).delete()
        for flow in tree.findall(".//bpmn:sequenceFlow", namespaces=ns):
            source_ref = flow.attrib['sourceRef']
            target_ref = flow.attrib['targetRef']
            try:
                if source_ref in element_mapping and target_ref in element_mapping:
                    ProcessLink.objects.create(
                        start_element=element_mapping[source_ref],
                        end_element=element_mapping[target_ref],
                        link_type='sequenceFlow'
                    )
                    logger.info(f"Линк создан: {source_ref} -> {target_ref}")
                else:
                    logger.warning(f"Пропущен линк, не найдены элементы: {source_ref} или {target_ref}")
            except Exception as e:
                logger.error(f"Ошибка при создании линка {source_ref} -> {target_ref}: {e}")
                raise

    def patch(self, request, pk):
        logger.debug(f"request.data: {request.data}")
        try:
            logger.debug(f"Получен запрос для обновления XML: {request.data}")
            # Get the process instance using the pk parameter
            try:
                process_instance = Process.objects.get(pk=pk)
            except Process.DoesNotExist:
                logger.error(f"Процесс с id={pk} не найден")
                return Response({"error": f"Процесс с id={pk} не найден"}, status=404)

            xml_data = BpmnXmlProcess.objects.filter(id=request.data.get("bpmn_xml")).values_list("xml", flat=True).first()
            if not xml_data:
                logger.error("XML не передан в запросе")
                return Response({"error": "XML не передан"}, status=400)

            logger.debug(f"Обновляем XML для процесса {process_instance.id}")
            # Update the XML content
            process_instance.bpmn_xml.xml = xml_data
            process_instance.bpmn_xml.save()

            # Parse and sync the updated XML
            self.parse_and_sync_xml(process_instance)
            return Response({"message": "XML обновлён и элементы синхронизированы"})
        except Exception as e:
            logger.error(f"Ошибка при обновлении XML: {e}")
            return Response({"error": str(e)}, status=500)

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


