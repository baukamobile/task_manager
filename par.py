import os
import django
import xml.etree.ElementTree as ET
from bpm.models import ProcessElement, ProcessLink

# Настройка окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')

# Инициализация Django
django.setup()

def parse_xml(xml_str, process_instance):
    ns = {
        'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
        'bpmndi': 'http://www.omg.org/spec/BPMN/20100524/DI',
        'di': 'http://www.omg.org/spec/DD/20100524/DI'
    }

    tree = ET.fromstring(xml_str)
    element_mapping = {}

    # Определяем порядок элементов: сначала события, потом задачи и шлюзы
    element_order = ['startEvent', 'task', 'parallelGateway', 'endEvent']

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

    print(f"Created elements in order: {element_mapping}")

    # Создание связей между элементами
    for flow in tree.findall(".//bpmn:sequenceFlow", namespaces=ns):
        source_ref = flow.attrib['sourceRef']
        target_ref = flow.attrib['targetRef']

        # Проверяем, что source и target элементы существуют в element_mapping
        if source_ref in element_mapping and target_ref in element_mapping:
            ProcessLink.objects.create(
                start_element=element_mapping[source_ref],
                end_element=element_mapping[target_ref],
                link_type='sequenceFlow'
            )
            print(f"Created link: {source_ref} -> {target_ref}")
        else:
            print(f"Warning: Element not found for source_ref={source_ref} or target_ref={target_ref}")

    print(f"Finished processing XML for {process_instance}")
