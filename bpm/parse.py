import xml.etree.ElementTree as ET

tree = ET.parse('empty.xml')
root = tree.getroot()

# Определяем пространство имен
namespaces = {'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL'}

# Ищем все элементы с тегом 'bpmn:sequenceFlow'
for task in root.findall('.//bpmn:process', namespaces=namespaces):
    print(f'taskkks {task.tag}')



