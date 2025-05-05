from django.db import models
from django.db import models
from django.utils import timezone
from users.models import User,Department
import logging
from simple_history.models import HistoricalRecords
import xml.etree.ElementTree as et

logger = logging.getLogger('bpm')

class Process(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('running', 'Выполняется'),
        ('completed', 'Завершён'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True, related_name='owned_processes')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='processes',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    current_task = models.ForeignKey('Task',on_delete=models.SET_NULL,null=True,blank=True, related_name='current_task')
    bpmn_xml = models.ForeignKey('BpmnXmlProcess', null=True,blank=True, on_delete=models.SET_NULL,related_name='processes')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending',null=True,blank=True)
    bpmn_process_id = models.CharField(max_length=100,null=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.name
    def save(self,*args,**kwargs):
        '''При создании процесса
        автоматический создается новый пустой bpmn xml чтобы когда пользователь меняет диаграмму не исчезло данные'''
        if not self.bpmn_xml:
            xml_obj = BpmnXmlProcess.objects.create()
            self.bpmn_xml = xml_obj
            logger.info('При создании процесса автоматический создается новый пустой bpmn xml')
        super().save(*args,**kwargs)

    class Meta:
        permissions = [
            ('start_process','Может запускать процесс'),
            ('approve_process', 'Может одобрять  процесс'),
            ('execute_process', 'Может выполнять  процесс'),
            ('finish_process', 'Может завершать  процесс'),
        ]
class Task(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Не начата'),
        ('in_progress', 'В работе'),
        ('blocked', 'Заблокирована'),
        ('completed', 'Выполнена'),
        ('returned', 'Возвращена на доработку'),
    ]
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='tasks')
    # title = models.CharField(max_length=200)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    assigned_department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,related_name='assigned_department')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    return_reason = models.TextField(null=True,blank=True)
    '''это про внутреннее состояние задачи. На том же этапе "Проверка" она может быть "Не начата" 
     (лежит мёртвым грузом), "В работе" (кто-то её ковыряет) или 
     "Заблокирована" (ждёт, пока Вася принесёт документы).'''
    due_date = models.DateTimeField(null=True, blank=True) # дедлайн
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True,blank=True)
    bpmn_task_id = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.status
    def is_overdue(self):
        if self.due_date and timezone.now() > self.due_date:
            return True
        return False
    def send_email_to_assigned_user(self):
        if self.assigned_to.is_valid():
            pass

def empty_xml():
    return '<?xml version="1.0" encoding="UTF-8"?> <bpmn:definitions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" targetNamespace="http://bpmn.io/schema/bpmn" id="Definitions_1"> <bpmn:process id="Process_1" isExecutable="false"> <bpmn:startEvent id="StartEvent_1"/> </bpmn:process> <bpmndi:BPMNDiagram id="BPMNDiagram_1"> <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Process_1"> <bpmndi:BPMNShape id="_BPMNShape_StartEvent_2" bpmnElement="StartEvent_1"> <dc:Bounds height="36.0" width="36.0" x="173.0" y="102.0"/></bpmndi:BPMNShape></bpmndi:BPMNPlane></bpmndi:BPMNDiagram></bpmn:definitions>'
class BpmnXmlProcess(models.Model):
    xml = models.TextField(default=empty_xml)

class ProcessElement(models.Model):

    ELEMENT_TYPES = [
        ('startEvent', 'Начальное событие'),
        ('endEvent', 'Конечное событие'),
        ('task', 'Задача'),
        ('parallelGateway', 'И'),
        ('exclusiveGateway', 'ИЛИ'),
        ('sequenceFlow', 'Стрелка'),
        ('text','Комментарий'),
        ('textAnnotation','Текстовое примечание'),
        # Можно позже добавить другие типы: 'gateway' и т.д.
    ]
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='elements')
    element_id = models.CharField(max_length=100)
    element_type = models.CharField(max_length=20, choices=ELEMENT_TYPES)
    name = models.CharField(max_length=100,null=True,blank=True)
    annotation = models.TextField(blank=True, null=True)  # For <bpmn:textAnnotation>

    # next_element = models.JSONField(default=list,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.get_element_type_display()}: {self.name}"
    # def save(self,*args,**kwargs):
    #     super().save(*args,**kwargs)
        # parse_bpmn_xml_and_save(self)
class ProcessLink(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    start_element = models.ForeignKey(ProcessElement, related_name='start_element', on_delete=models.CASCADE)
    end_element = models.ForeignKey(ProcessElement, related_name='end_element', on_delete=models.CASCADE)
    source_type = models.CharField(max_length=100,null=True)
    target_type = models.CharField(max_length=100,null=True)
    link_type = models.CharField(max_length=100, default='sequenceFlow')
    condition_expression = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Attachment(models.Model):
    """Вложения к задачам,вложения к задачам (файлы)."""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    filename = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename

class Comment(models.Model):
    """Комментарии к задачам. Комментарии к задачам от пользователей."""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.task}"


class Notification(models.Model):
    """Уведомления для пользователей. Уведомления для пользователей о различных событиях
    (дедлайны, назначения задач и т.д.)."""
    TYPE_CHOICES = [
        ('deadline', 'Приближение дедлайна'),
        ('overdue', 'Просроченная задача'),
        ('escalation', 'Эскалация задачи'),
        ('assignment', 'Назначена новая задача'),
        ('stage_change', 'Изменение этапа задачи'),
        ('comment', 'Новый комментарий'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    history = HistoricalRecords()
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user}: {self.message[:30]}..."

class Dashboard(models.Model):
    """Дашборды для руководства. Модели для создания информационных
    панелей с виджетами для руководства."""
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True, related_name='dashboards')
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class DashboardWidget(models.Model):
    """Виджеты на дашбордах, модели для создания информационных панелей с виджетами для руководства."""
    WIDGET_TYPES = [
        ('task_count', 'Количество задач'), #Показывает количество задач (например, общее, по статусам, по исполнителям)
        ('process_time', 'Время выполнения процессов'), #Отображает время выполнения процессов (например, среднее время прохождения задачи по всем этапам)
        ('overdue_tasks', 'Просроченные задачи'), #Показывает просроченные задачи (те, которые вышли за дедлайн)
        ('efficiency', 'Эффективность сотрудников'), #Визуализирует эффективность сотрудников (например, количество выполненных задач, время выполнения)
        ('bottlenecks', 'Узкие места'), #Выявляет "узкие места" в процессах (этапы, на которых задачи застревают дольше всего)
    ]

    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='widgets') #Связь с дашбордом, на котором размещен виджет
    title = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    position_x = models.PositiveSmallIntegerField(default=0,null=True, blank=True)
    position_y = models.PositiveSmallIntegerField(default=0,null=True,blank=True) # Координаты расположения виджета на дашборде
    width = models.PositiveSmallIntegerField(null=True, blank=True)
    height = models.PositiveSmallIntegerField(null=True, blank=True) #Ширина и высота виджета
    settings = models.JSONField(default=dict,null=True,blank=True) #JSON-поле для хранения дополнительных настроек виджета (фильтры, параметры отображения и т.д.)

    def __str__(self):
        return f"{self.title} on {self.dashboard.name}"

# class WorkflowRule(models.Model):
#     '''Правила переходов между этапами '''
#     process = models.ForeignKey('Process',on_delete=models.CASCADE,related_name="rules")
#     from_step = models.ForeignKey('ProcessStage', on_delete=models.CASCADE, related_name='transitions_from')
#     to_step = models.ForeignKey('ProcessStage', on_delete=models.CASCADE,related_name="transitions_to")
#     allowed_position = models.ForeignKey(Positions, on_delete=models.CASCADE)  # Кто может менять статус
#     def __str__(self):
#         return f"{self.from_step} → {self.to_step} ({self.allowed_position})"
#
# class ProcessTemplate(models.Model):
#     """Шаблоны бизнес-процессов.
#      шаблоны бизнес-процессов, которые можно использовать для
#      создания конкретных экземпляров процессов. Связаны с отделами и пользователями.
#     """
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='templates',null=True,blank=True)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     def __str__(self):
#         return f"{self.name} - {self.department}"
#
# class ProcessStageTemplate(models.Model):
#     """Шаблоны этапов бизнес-процессов
#      шаблоны этапов для каждого шаблона бизнес-процесса.
#      Содержат информацию о порядке, критериях завершения и SLA (часы на выполнение).
#     """
#     template = models.ForeignKey(ProcessTemplate,null=True,blank=True, on_delete=models.CASCADE, related_name='stages')
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=True, null=True)
#     order = models.PositiveIntegerField()
#     is_required = models.BooleanField(default=True)  # нельзя пропустить этап
#     completion_criteria = models.TextField(blank=True, null=True)  # условия для завершения этапа
#     sla_hours = models.PositiveIntegerField(default=24)  # SLA (Service Level Agreement — соглашение об уровне обслуживания
#
#     class Meta:
#         ordering = ['order']
#
#     def __str__(self):
#         return f"{self.template.name} - {self.name}"
# class ProcessStage(models.Model):
#     """Этапы конкретного бизнес-процесса (колонки Kanban)
#      этапы конкретного бизнес-процесса (колонки Kanban-доски). Могут быть созданы на основе шаблонов этапов.
#     """
#     process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='stages')
#     template_stage = models.ForeignKey(ProcessStageTemplate, on_delete=models.SET_NULL, null=True,blank=True)
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=True, null=True)
#     order = models.PositiveIntegerField()
#     is_required = models.BooleanField(default=True)
#     completion_criteria = models.TextField(blank=True, null=True)
#     sla_hours = models.PositiveIntegerField(default=24) #SLA (Service Level Agreement — соглашение об уровне обслуживания
#     is_custom = models.BooleanField(default=False)  # кастомный этап или из шаблона
#     is_key_stage = models.BooleanField(default=False)  # Ключевой этап или промежуточный
#     class Meta:
#         ordering = ['order']
#     def __str__(self):
#         return f"{self.process.name} - {self.name}"

    # def move_task(task, new_stage, user):
    #     current_rule = WorkflowRule.objects.filter(
    #         process=task.process,
    #         stages=task.current_stage,
    #         allowed_position=user.position
    #     ).first()
    #     new_rule = WorkflowRule.objects.filter(
    #         process=task.process,
    #         stages=new_stage,
    #         allowed_position=user.position
    #     ).first()
    #     if current_rule and new_rule and current_rule == new_rule:
    #         if new_stage.order > task.current_stage.order:  # Проверяем порядок
    #             task.current_stage = new_stage
    #             task.save()
    #         else:
    #             raise Exception("Назад нельзя!")
    #     else:
    #         raise Exception("Нет прав или правила!")
    # def move_task(task, new_stage, user):
    #     current = task.current_stage
    #     if new_stage.order <= current.order:
    #         raise Exception("Назад нельзя!")
    #
    #     # Если оба этапа ключевые, проверяем правило
    #     if current.is_key_stage and new_stage.is_key_stage:
    #         rule = WorkflowRule.objects.filter(
    #             process=task.process,
    #             from_step=current,
    #             to_step=new_stage,
    #             allowed_position=user.position
    #         ).first()
    #         if not rule:
    #             raise Exception("Нет прав или правила!")
    #
    #     # Проверяем, что новый этап следующий по порядку
    #     next_stage = ProcessStage.objects.filter(
    #         process=task.process,
    #         order__gt=current.order
    #     ).order_by('order').first()
    #     if next_stage == new_stage:
    #         task.current_stage = new_stage
    #         task.save()
    #     else:
    #         raise Exception("Скачки запрещены!")
# class TaskStageHistory(models.Model):
#     """История перемещения задачи между этапами.
#      история перемещения задач между этапами, что позволяет отслеживать весь путь задачи.
#     """
#     task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='stage_history')
#     from_stage = models.ForeignKey(ProcessStage, on_delete=models.SET_NULL, null=True,
#                                    related_name='from_stage_history')
#     to_stage = models.ForeignKey(ProcessStage, on_delete=models.SET_NULL, null=True, related_name='to_stage_history')
#     changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     changed_at = models.DateTimeField(auto_now_add=True)
#     comments = models.TextField(blank=True, null=True)
#     class Meta:
#         ordering = ['-changed_at']
#
#     def __str__(self):
#         return f"Task {self.task.id}: {self.from_stage} -> {self.to_stage}"
#
# class AutoTaskRule(models.Model):
#     """Правила автоматического создания подзадач.
#      правила для автоматического создания подзадач при достижении определенных этапов.
#     """
#     trigger_stage = models.ForeignKey(ProcessStage, on_delete=models.CASCADE, related_name='triggered_rules')
#     source_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='source_rules',null=True, blank=True)
#     target_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='target_rules',null=True, blank=True)
#     target_template = models.ForeignKey(ProcessTemplate, on_delete=models.CASCADE, related_name='rules')
#     description = models.TextField()
#     is_active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return f"Rule: {self.source_department} -> {self.target_department} on {self.trigger_stage.name}"



# class ProcessElement(models.Model):

#     ELEMENT_TYPES = [
#         ('start_event', 'Начальное событие'),
#         ('end_event', 'Конечное событие'),
#         ('task', 'Задача'),
#         # Можно позже добавить другие типы: 'gateway', 'parallel_task' и т.д.
#     ]
#     process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='elements')
#     element_type = models.CharField(max_length=20, choices=ELEMENT_TYPES)
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=True, null=True)
#     position_x = models.IntegerField(default=0)  # Координаты на диаграмме
#     position_y = models.IntegerField(default=0)
#     assigned_role = models.ForeignKey(Positions, on_delete=models.SET_NULL, null=True, blank=True)  # Кто выполняет
#     stage = models.ForeignKey(ProcessStage, on_delete=models.SET_NULL, null=True, blank=True, related_name='elements')
#
#     def __str__(self):
#         return f"{self.get_element_type_display()}: {self.name}"
#
# class ElementConnection(models.Model):
#     """Связи между элементами процесса (стрелки на диаграмме)"""
#     source = models.ForeignKey(ProcessElement, on_delete=models.CASCADE, related_name='outgoing_connections')
#     target = models.ForeignKey(ProcessElement, on_delete=models.CASCADE, related_name='incoming_connections')
#     label = models.CharField(max_length=100, blank=True, null=True)  # Подпись на стрелке
#     condition = models.TextField(blank=True, null=True)  # Условие перехода (для будущего использования)
#
#     def __str__(self):
#         return f"{self.source.name} → {self.target.name}"
#
# class ProcessExecution(models.Model):
#     """Экземпляр выполнения процесса"""
#     process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='executions')
#     started_at = models.DateTimeField(auto_now_add=True)
#     completed_at = models.DateTimeField(null=True, blank=True)
#     current_element = models.ForeignKey(ProcessElement, on_delete=models.SET_NULL, null=True, related_name='executions')
#     status = models.CharField(max_length=20, default='active', choices=[
#         ('active', 'Активен'),
#         ('completed', 'Завершен'),
#         ('terminated', 'Прерван'),
#     ])
#
#     def __str__(self):
#         return f"Execution of {self.process.name} ({self.status})"









