from rest_framework import serializers
from tasks.models import Task,Status,Projects
from users.serializers import UserSerializer

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    def validate_end_date(self, value):
        print(f"end_date в сериализаторе: {value}")  # Посмотрим, что реально пришло
        return value
    class Meta:
        model = Task
        fields = '__all__'
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id','status_name','project']

