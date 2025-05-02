import logging
import xml.etree.ElementTree as ET
from bpm.models import *
from rest_framework.views import APIView

from bpm.serializers import *
from rest_framework.viewsets import ModelViewSet
logger = logging.getLogger('bpm')

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
            try:
                element, _ = ProcessElement.objects.update_or_create(
                    process=process_instance,
                    element_id=el_id,
                    defaults={
                        'element_type': tag,
                        'name': name,
                    }
                )
                element_mapping[el_id] = element
                logger.info(f"{'Создан' if _ else 'Обновлён'} элемент: {el_id} - {name}")
            except Exception as e:
                logger.error(f"Ошибка при сохранении элемента {el_id}: {e}")
                raise