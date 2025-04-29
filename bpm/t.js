const saveDiagram = async () => {
    try {
      const { xml } = await modeler.value.saveXML({ format: true });
      console.log('Сохранённый XML:', xml);
  
      // Находим текущий процесс
      const process = processes.value.find(p => p.id === selectedProcessId.value);
      if (!process) {
        throw new Error('Процесс не найден');
      }
  
      // Если у процесса уже есть bpmn_xml, обновляем существующую запись
      if (process.bpmn_xml) {
        const response = await axios.patch(`${API_BPMNXML_PROCESS}${process.bpmn_xml}/`, {
          xml,
        });
        console.log('Диаграмма обновлена на сервере:', response.data);
      } else {
        // Если bpmn_xml отсутствует, создаём новую запись
        const response = await axios.post(`${API_BPMNXML_PROCESS}`, {
          process_id: selectedProcessId.value,
          xml,
        });
        console.log('Диаграмма создана на сервере:', response.data);
  
        // Обновляем локальный processes с новым bpmn_xml ID
        process.bpmn_xml = response.data.id;
      }
    } catch (err) {
      console.error('Ошибка сохранения:', err);
    }
  };