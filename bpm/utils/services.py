import logging
import xml.etree.ElementTree as ET
from bpm.models import *
from rest_framework.views import APIView

from bpm.serializers import *
from rest_framework.viewsets import ModelViewSet
logger = logging.getLogger('bpm')
def parse_and_sync_xml(process_instance): #функция для парсинга bpmn диаграмму
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
    element_order = ['startEvent', 'task', 'parallelGateway', 'exclusiveGateway', 'textAnnotation', 'sequenceFlow',
                     'endEvent']
    for tag in element_order:
        for elem in tree.findall(f".//bpmn:{tag}", namespaces=ns):
            el_id = elem.attrib['id']
            name = elem.attrib.get('name')
            annotation = elem.find("bpmn:text", namespaces=ns).text if elem.find("bpmn:text", namespaces=ns) is not None else ''
            try:
                element, _ = ProcessElement.objects.update_or_create(
                    process=process_instance,
                    element_id=el_id,
                    defaults={
                        'element_type': tag,
                        'name': name,
                        'annotation': annotation,
                    }
                )
                element_mapping[el_id] = element
                logger.info(f"{'Создан' if _ else 'Обновлён'} элемент: {el_id} - {name} - {annotation}")
                if tag == 'task':
                    task,created = Task.objects.update_or_create(
                        process = process_instance,
                        bpmn_task_id = el_id,
                        defaults={
                            'assigned_to': None,
                            'assigned_department': None,
                            'status': 'in_progress',
                            'due_date': None,
                            'return_reason': None,
                            'completed_at': None
                        }
                    )
                    logger.info(f"{'Задача создана' if created else 'Задача обновлена'} для элемента {el_id}")
            except Exception as e:
                logger.error(f"Ошибка при сохранении элемента {el_id}: {e}")
                raise
 # Удаляем старые связи перед созданием новых, иначе будут дублироваться
    ProcessLink.objects.filter(start_element__process=process_instance).delete()
    for flow in tree.findall(".//bpmn:sequenceFlow", namespaces=ns):
        source_ref = flow.attrib['sourceRef']
        target_ref = flow.attrib['targetRef']
        source_type = element_mapping[source_ref].element_type
        target_type = element_mapping[target_ref].element_type
        try:
            if source_ref in element_mapping and target_ref in element_mapping:
                ProcessLink.objects.update_or_create(
                     process=process_instance,
                    start_element=element_mapping[source_ref],
                    end_element=element_mapping[target_ref],
                    link_type='sequenceFlow',
                    source_type=source_type,
                    target_type=target_type,
                )
                logger.info(f"Связь создан: {source_ref} -> {target_ref}")
            else:
                logger.warning(f"Пропущен связь, не найдены элементы: {source_ref} или {target_ref}")
        except Exception as e:
            logger.error(f"Ошибка при создании линка {source_ref} -> {target_ref}: {e}")
            raise