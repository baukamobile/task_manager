from rest_framework.generics import ListAPIView

from django.shortcuts import render
from tasks.models import Task
from tasks.serializers import TaskSerializer


class TaskListView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer











