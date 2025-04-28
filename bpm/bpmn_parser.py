import xml.etree.ElementTree as ET
from bpm.models import ProcessElement

def parse_bpmn_xml_and_save(process):
    """Парсит BPMN XML и сохраняет элементы в базу."""
    xml_content = process.bpmn_xml.xml
    tree = ET.ElementTree(ET.fromstring(xml_content))
    root = tree.getroot()

    # Прочитаем все элементы
    for elem in root.iter():
        tag = elem.tag.split('}')[-1]  # Убираем неймспейсы типа {http://...}

        if tag in ['startEvent', 'endEvent', 'task', 'userTask', 'parallelGateway']:
            element_id = elem.attrib.get('id')
            name = elem.attrib.get('name', None)

            if tag == 'userTask' or tag == 'task':
                element_type = 'task'
            else:
                element_type = tag.lower()  # start_event, end_event, parallel_gateway

            ProcessElement.objects.create(
                process=process,
                element_id=element_id,
                name=name,
                element_type=element_type,
                next_elements=[]  # пока пусто, потом заполним
            )
