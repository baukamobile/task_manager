from rest_framework.generics import ListAPIView

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from tasks.models import Task
from tasks.serializers import TaskSerializer


class TaskListView(ListAPIView): #если пользователь админ
    permission_classes = [IsAdminUser]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

def taskpage(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task.html',context={'tasks':tasks})









