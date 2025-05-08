import logging
import xml.etree.ElementTree as ET
from bpm.models import *
from rest_framework.views import APIView

from bpm.serializers import *
from rest_framework.viewsets import ModelViewSet
logger = logging.getLogger('bpm')
from collections import deque

def parse_and_sync_xml(process_instance):
    bpmn_xml_obj = process_instance.bpmn_xml
    xml_str = bpmn_xml_obj.xml #Вытаскиваем сырой XML из объекта процесса
    ns = { #Пространства имён XML  необходимое для поиска элементов через XPath.
        'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
        'bpmndi': 'http://www.omg.org/spec/BPMN/20100524/DI',
        'di': 'http://www.omg.org/spec/DD/20100524/DI'
    }
    try:
        tree = ET.fromstring(xml_str)
        logger.info(f"XML парсуется для процесса: {process_instance}")
    except ET.ParseError as e:
        logger.error(f"Ошибка парсинга XML: {e}")
        raise

    element_mapping = {} #для связи id элемента BPMN с объектом ProcessElement.
    graph = {} #структура для хранения информации об элементах и их исходящих связях.
    flows = [] #список связей между элементами, которые будут обрабатываться отдельно
    for elem in tree.findall(".//bpmn:*", namespaces=ns):
        tag = elem.tag.split('}')[-1]
        if tag in ['startEvent', 'task', 'parallelGateway', 'exclusiveGateway', 'textAnnotation', 'endEvent']: #узлы bpmn
            el_id = elem.attrib['id']
            name = elem.attrib.get('name', '')
            annotation = elem.find("bpmn:text", namespaces=ns).text if elem.find("bpmn:text", namespaces=ns) is not None else ''
            graph[el_id] = {
                'type': tag,
                'name': name,
                'annotation': annotation,
                'outgoing': []
            }
        elif tag == 'sequenceFlow': #ребра
            source_ref = elem.attrib['sourceRef']
            target_ref = elem.attrib['targetRef']
            flow_id = elem.attrib['id']
            flows.append((source_ref, target_ref,flow_id))

    for source_ref, target_ref, flow_id in flows:
        if source_ref in graph and target_ref in graph:
            graph[source_ref]['outgoing'].append(target_ref)
        else:
            logger.warning(f"Пропущена связь: {source_ref} -> {target_ref} (flow id: {flow_id})")

    start_event = None
    for el_id, data in graph.items():
        if data['type'] == 'startEvent':
            start_event = el_id
            break
    if not start_event:
        logger.error("startEvent не найден")
        raise ValueError("No startEvent found")
    queue = deque([start_event])
    visited = set()
    while queue:
        el_id = queue.popleft()
        if el_id in visited:
            continue
        visited.add(el_id)
        data = graph[el_id]

        try:
            element, created = ProcessElement.objects.update_or_create(
                process=process_instance,
                element_id=el_id,
                defaults={
                    'element_type': data['type'],
                    'name': data['name'],
                    'annotation': data['annotation']
                }
            )
            element_mapping[el_id] = element
            logger.info(f"{'Создан' if created else 'Обновлён'} элемент: {el_id} - {data['name']} {data['annotation']}")

            if data['type'] == 'task':
                task, created = Task.objects.update_or_create(
                    process=process_instance,
                    bpmn_task_id=el_id,
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

        for next_id in data['outgoing']:
            if next_id not in visited:
                queue.append(next_id)

    ProcessLink.objects.filter(start_element__process=process_instance).delete()
    for source_ref, target_ref,flow_id in flows:
        try:
            if source_ref in element_mapping and target_ref in element_mapping:
                ProcessLink.objects.update_or_create(
                    process=process_instance,
                    start_element=element_mapping[source_ref],
                    end_element=element_mapping[target_ref],
                    element_id=flow_id,
                    link_type='sequenceFlow',
                    source_type=element_mapping[source_ref].element_type,
                    target_type=element_mapping[target_ref].element_type,
                )
                logger.info(f"Связь создана: {source_ref} -> {target_ref}, {flow_id}")
            else:
                logger.warning(f"Пропущена связь, не найдены элементы: {source_ref} или {target_ref}")
        except Exception as e:
            logger.error(f"Ошибка при создании связи {source_ref} -> {target_ref}: {e}")
            raise