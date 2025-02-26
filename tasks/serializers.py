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
    class Meta:
        model = Status
        fields = '__all__'