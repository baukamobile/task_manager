from rest_framework.views import APIView

from bpm.serializers import *
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from par import parse_xml
from bpm.models import BpmnXmlProcess
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Process, BpmnXmlProcess, ProcessElement, ProcessLink
from .serializers import ProcessSerializer
import logging

logger = logging.getLogger('bpm')

class BpmXmlProcessViewSet(ModelViewSet):
    queryset = BpmnXmlProcess.objects.all()
    logger.info('bpmn xml processviewset')
    serializer_class = BpmnXmlProcessSerializer
    @csrf_exempt
    def create(self, request, *args, **kwargs):
        xml = request.data.get('xml')
        instance = BpmnXmlProcess.objects.create(xml=xml)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    logger.info("Task viewset")
    serializer_class = TaskSerializer

class AttachmentViewSet(ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class ProcessElementViewSet(ModelViewSet):
    queryset = ProcessElement.objects.all()
    serializer_class = ProcessElementSerializer
