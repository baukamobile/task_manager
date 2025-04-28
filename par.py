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

    # Пример вывода для отладки
    print(f"Parsing XML for process: {process_instance}")

    for tag in ['task', 'startEvent', 'endEvent', 'parallelGateway']:
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

    print(f"Created elements: {element_mapping}")

    for flow in tree.findall(".//bpmn:sequenceFlow", namespaces=ns):
        source_ref = flow.attrib['sourceRef']
        target_ref = flow.attrib['targetRef']
        ProcessLink.objects.create(
            start_element=element_mapping[source_ref],
            end_element=element_mapping[target_ref],
            link_type='sequenceFlow'
        )

    print(f"Finished processing XML for {process_instance}")
