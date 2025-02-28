from rest_framework.generics import ListAPIView,RetrieveAPIView,RetrieveUpdateAPIView,CreateAPIView,DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from tasks.models import Task, Status, Projects
from tasks.serializers import TaskSerializer, StatusSerializer,ProjectSerializer


class TaskViewSet(ModelViewSet):  # Отдаёт список всех задач
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    http_method_names = ['get','post','put','patch','delete']

# class TaskDetailView(RetrieveUpdateAPIView):  # Отдаёт конкретную задачу
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer


class StatusViewSet(ModelViewSet):
    # permission_classes = [IsAdminUser]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

# class StatusDetailView(RetrieveUpdateAPIView):
#     # permission_classes = [IsAdminUser]
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer



class ProjectViewSet(ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer

