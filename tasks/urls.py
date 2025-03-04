from django.urls import path,include
from rest_framework.routers import DefaultRouter
from tasks.views import (TaskViewSet,ProjectViewSet,StatusViewSet)
router = DefaultRouter()
router.register(r'status',StatusViewSet),
router.register(r'tasks',TaskViewSet),
router.register(r'projects',ProjectViewSet)
urlpatterns = [
    path('',include(router.urls)),
    # path('api/task-stats/', task_statistics),


    # path('',taskpage),
]