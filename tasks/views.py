from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count
from rest_framework.response import Response

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

#admin panel статиска не закончен нужен frontend vuejs
# @api_view(['GET'])
# def task_statistics(request):
#     stats = Task.objects.annotate(task_count=Count('task'))
#     data = [
#         {
#             "название задачи": task.title,
#             "задачи": task.task_count
#         }
#         for task in stats
#     ]
#     return Response({"задачи": data})
