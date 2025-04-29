import os
import django
import xml.etree.ElementTree as ET
from bpm.models import ProcessElement, ProcessLink
import logging
# Настройка окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')

# Инициализация Django
django.setup()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_xml(self,xml_str, process_instance):
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