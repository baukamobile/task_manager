import xml.etree.ElementTree as ET
from bpm.models import ProcessElement, ProcessLink


def parse_bpmn_xml_and_save(process):
    """Парсит BPMN XML и сохраняет элементы в базу данных."""

    xml_content = process.bpmn_xml.xml  # Получаем XML
    print("Парсим XML...")

    try:
        tree = ET.ElementTree(ET.fromstring(xml_content))
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Ошибка при парсинге XML: {e}")
        return

    # Словарь для хранения элементов по ID
    elements_by_id = {}

    # Парсим все элементы BPMN
    for elem in root.iter():
        tag = elem.tag.split('}')[-1]  # Убираем неймспейсы

        if tag in ['startEvent', 'endEvent', 'task', 'userTask', 'parallelGateway']:
            element_id = elem.attrib.get('id')
            name = elem.attrib.get('name', None)
            print(f"Найден элемент: {tag}, ID: {element_id}, Name: {name}")

            # Определяем тип элемента
            if tag in ['userTask', 'task']:
                element_type = 'task'
            else:
                element_type = tag.lower()  # start_event, end_event, parallel_gateway

            # Сохраняем элемент в базу данных
            process_element = ProcessElement.objects.create(
                process=process,
                element_id=element_id,
                name=name,
                element_type=element_type,
                next_element=[]  # Пока пусто, позже добавим связи
            )

            # Добавляем элемент в словарь по его ID
            elements_by_id[element_id] = process_element

    # Теперь добавляем связи (next_elements) между элементами
    for elem in root.iter():
        tag = elem.tag.split('}')[-1]

        if tag in ['startEvent', 'endEvent', 'task', 'userTask', 'parallelGateway']:
            element_id = elem.attrib.get('id')
            outgoing_elements = elem.findall('.//bpmn:outgoing',
                                             namespaces={'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL'})

            # Получаем все ID исходящих элементов
            next_elements = []
            for outgoing in outgoing_elements:
                next_elements.append(outgoing.text)

            # Обновляем связи для текущего элемента
            if element_id in elements_by_id:
                process_element = elements_by_id[element_id]
                process_element.next_elements = next_elements
                process_element.save()

                # Создаем связи в модели ProcessLink
                for next_element_id in next_elements:
                    if next_element_id in elements_by_id:
                        next_element = elements_by_id[next_element_id]
                        ProcessLink.objects.create(
                            start_element=process_element,
                            end_element=next_element
                        )

    print("Парсинг завершён.")
