from rest_framework.generics import ListAPIView,RetrieveAPIView,RetrieveUpdateAPIView,CreateAPIView

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from tasks.models import Task, Status, Projects
from tasks.serializers import TaskSerializer, StatusSerializer,ProjectSerializer


class TaskListView(ListAPIView):  # Отдаёт список всех задач
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailView(RetrieveUpdateAPIView):  # Отдаёт конкретную задачу
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskAddView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class StatusListView(ListAPIView):
    # permission_classes = [IsAdminUser]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class StatusDetailView(RetrieveUpdateAPIView):
    # permission_classes = [IsAdminUser]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class StatusAddView(CreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class ProjectListView(ListAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer

class ProjectAddView(CreateAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer