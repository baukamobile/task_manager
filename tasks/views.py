from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import json

from tasks.models import Task, Status, Projects
from tasks.serializers import TaskSerializer, StatusSerializer,ProjectSerializer


class TaskViewSet(ModelViewSet):  # Отдаёт список всех задач
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get','post','put','patch','delete']
    def create(self, request, *args, **kwargs):
        print("Полученные данные:", json.dumps(request.data, indent=4, ensure_ascii=False))  # ЛОГ ЗАПРОСА

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("💀 Ошибки сериализации:", serializer.errors)  # ЛОГ ОШИБОК
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        # получение статусов по айди проекта
        project_id = self.request.query_params.get("project")
        queryset = Task.objects.all()

        if project_id:
            queryset = queryset.filter(project__id=project_id)  # <-- Вот здесь исправил

        return queryset
# class TaskDetailView(RetrieveUpdateAPIView):  # Отдаёт конкретную задачу
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer


class StatusViewSet(ModelViewSet):
    # permission_classes = [IsAdminUser]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def get_queryset(self):
        project_id = self.request.query_params.get("project")
        queryset = Status.objects.all()

        if project_id:
            queryset = queryset.filter(project_id=project_id)

        return queryset

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
