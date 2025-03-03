from rest_framework import serializers
from tasks.models import Task,Status,Projects
from users.serializers import UserSerializer

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    class Meta:
        model = Task
        fields = '__all__'
class StatusSerializer(serializers.ModelSerializer):
    # status = serializers.SlugRelatedField(read_only=True, slug_field='name')
    # class Meta:
    #     model = Status
    # priority_name = serializers.CharField(source='priority.name',read_only=True)
    # user = UserSerializer()
    class Meta:
        model = Status
        fields = ['id','status_name','user']

