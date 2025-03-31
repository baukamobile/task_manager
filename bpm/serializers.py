from rest_framework import serializers
from bpm.models import Process,WorkflowStep

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = '__all__'
class WorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowStep
        fields = '__all__'