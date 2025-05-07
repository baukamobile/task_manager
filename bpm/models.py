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
    # current_task = models.ForeignKey('Task',on_delete=models.SET_NULL,null=True,blank=True, related_name='current_task')
    active_tokens = models.ManyToManyField('Token',related_name='active_processes',blank=True)
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
    element = models.ForeignKey('ProcessElement', on_delete=models.CASCADE, related_name='tasks', null=True)
    due_date = models.DateTimeField(null=True, blank=True) # дедлайн
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True,blank=True)
    bpmn_task_id = models.CharField(max_length=100,null=True)
    is_completed = models.BooleanField(default=False)

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
        ('text','Комментарий'),
        ('textAnnotation','Текстовое примечание'),
        # Можно позже добавить другие типы: 'gateway' и т.д.
    ]
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='elements')
    element_id = models.CharField(max_length=100)
    element_type = models.CharField(max_length=20, choices=ELEMENT_TYPES)
    name = models.CharField(max_length=100,null=True,blank=True)
    annotation = models.TextField(blank=True, null=True)  # For <bpmn:textAnnotation>
    assigned = models.ForeignKey(User,on_delete=models.CASCADE,related_name='assigned',blank=True,null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [
            models.Index(fields=['process', 'element_id']),
            models.Index(fields=['element_type']),
        ]
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

    class Meta:
        indexes = [
            models.Index(fields=['process', 'start_element', 'end_element']),
        ]
class Token(models.Model):
    STATUS_CHOICES = [
        ('active','Активен'),
        ('completed','Завершен'),
    ]
    process = models.ForeignKey(Process,on_delete=models.CASCADE,related_name='tokens')
    element = models.ForeignKey(ProcessElement,on_delete=models.CASCADE,related_name='token')
    status = models.CharField(max_length=30,choices=STATUS_CHOICES,default='active')
    parent_token = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()
    class Meta:
        indexes = [
            models.Index(fields=['process', 'status']),
        ]

class GatewayCondition(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='conditions')
    element = models.ForeignKey(ProcessElement, on_delete=models.CASCADE, related_name='conditions')
    condition_type = models.CharField(max_length=50)  # Например, 'task_status', 'variable'
    condition_value = models.JSONField()  # { "task_id": "task_1", "status": "completed" }
    target_element = models.ForeignKey(ProcessElement, on_delete=models.CASCADE, related_name='condition_targets')
    priority = models.IntegerField(default=0)  # Порядок проверки условий Это упростит выбор условия в exclusiveGateway.

class Attachment(models.Model):
    """Вложения к задачам,вложения к задачам (файлы)."""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    filename = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename


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


