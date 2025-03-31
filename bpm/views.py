from django.shortcuts import render
from bpm.models import *
from bpm.serializers import ProcessSerializer,WorkflowStepSerializer
from rest_framework.viewsets import ModelViewSet
# Create your views here.
class ProcessViewSet(ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer

class WorkflowStepViewSet(ModelViewSet):
    queryset = WorkflowStep.objects.all()
    serializer_class = WorkflowStepSerializer








