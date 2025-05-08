import logging
import xml.etree.ElementTree as ET
from bpm.models import *
from rest_framework.views import APIView

from bpm.serializers import *
from rest_framework.viewsets import ModelViewSet
logger = logging.getLogger('bpm')
from collections import deque
from collections import deque

def parse_and_sync_xml(process_instance):
    bpmn_xml_obj = process_instance.bpmn_xml
    xml_str = bpmn_xml_obj.xml
    ns = {
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

    element_mapping = {}
    graph = {}
    flow_mapping = {}  # теперь тут будут храниться ID потока по ключу (source, target)

    for elem in tree.findall(".//bpmn:*", namespaces=ns):
        tag = elem.tag.split('}')[-1]
        if tag in ['startEvent', 'task', 'parallelGateway', 'exclusiveGateway', 'textAnnotation', 'endEvent']:
            el_id = elem.attrib['id']
            name = elem.attrib.get('name', '')
            annotation = elem.find("bpmn:text", namespaces=ns).text if elem.find("bpmn:text", namespaces=ns) is not None else ''
            graph[el_id] = {
                'type': tag,
                'name': name,
                'annotation': annotation,
                'outgoing': []
            }
        elif tag == 'sequenceFlow':
            source_ref = elem.attrib['sourceRef']
            target_ref = elem.attrib['targetRef']
            flow_id = elem.attrib['id']
            if source_ref in graph:
                graph[source_ref]['outgoing'].append(target_ref)
            flow_mapping[(source_ref, target_ref)] = flow_id

    # Удаляем старые связи
    ProcessLink.objects.filter(start_element__process=process_instance).delete()

    # Ищем старт и запускаем BFS
    start_event = next((el_id for el_id, data in graph.items() if data['type'] == 'startEvent'), None)
    if not start_event:
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

            if data['type'] == 'task':
                Task.objects.update_or_create(
                    process=process_instance,
                    bpmn_task_id=el_id,
                    defaults={
                        'assigned_to': None,
                        'assigned_department': None,
                        'status': 'in_progress',
                        'deadline': None,
                        'return_reason': None,
                        'completed_at': None
                    }
                )
        except Exception as e:
            logger.error(f"Ошибка при сохранении элемента {el_id}: {e}")
            raise

        for next_id in data['outgoing']:
            flow_id = flow_mapping.get((el_id, next_id))
            if flow_id and el_id in element_mapping and next_id in graph:
                try:
                    end_element = element_mapping.get(next_id)
                    if not end_element:
                        # Создаём конечный элемент, если он ещё не был обработан
                        end_data = graph[next_id]
                        end_element, _ = ProcessElement.objects.update_or_create(
                            process=process_instance,
                            element_id=next_id,
                            defaults={
                                'element_type': end_data['type'],
                                'name': end_data['name'],
                                'annotation': end_data['annotation']
                            }
                        )
                        element_mapping[next_id] = end_element

                    ProcessLink.objects.update_or_create(
                        process=process_instance,
                        start_element=element_mapping[el_id],
                        end_element=end_element,
                        element_id=flow_id,
                        link_type='sequenceFlow',
                        source_type=element_mapping[el_id].element_type,
                        target_type=end_element.element_type,
                    )
                except Exception as e:
                    logger.error(f"Ошибка при создании связи {el_id} -> {next_id}: {e}")
                    raise

            if next_id not in visited:
                queue.append(next_id)
