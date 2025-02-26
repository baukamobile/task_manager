from rest_framework.generics import ListAPIView,RetrieveAPIView,RetrieveUpdateAPIView

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from tasks.models import Task,Status
from tasks.serializers import TaskSerializer, StatusSerializer


class TaskListView(ListAPIView):  # Отдаёт список всех задач
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailView(RetrieveUpdateAPIView):  # Отдаёт конкретную задачу
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

def taskpage(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task.html',context={'tasks':tasks})


class StatusListView(ListAPIView):
    # permission_classes = [IsAdminUser]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class StatusDetailView(RetrieveUpdateAPIView):
    # permission_classes = [IsAdminUser]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer





