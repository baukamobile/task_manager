from rest_framework import serializers
from tasks.models import Task,Status
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
class StatusSerializer(serializers.ModelSerializer):
    # status = serializers.SlugRelatedField(read_only=True, slug_field='name')
    # class Meta:
    #     model = Status
    priority_name = serializers.CharField(source='priority.name',read_only=True)
    class Meta:
        model = Status
        fields = '__all__'