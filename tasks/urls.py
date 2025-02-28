from django.urls import path
from rest_framework.routers import DefaultRouter
from tasks.views import (TaskListView, StatusListView,
                         TaskDetailView,StatusDetailView,
                         TaskAddView,StatusAddView,ProjectListView,ProjectAddView)
router = DefaultRouter()
# router.register(r'status',StatusListView),
# router.register(r'tasks',TaskListView),
urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='tasks'),
    path('status/', StatusListView.as_view(), name='status'),
    path('status/<int:pk>/', StatusDetailView.as_view(), name='status'),
    path('tasks/add/',TaskAddView.as_view(), name='taskadd'),
    path('status/add/', StatusAddView.as_view(), name='statusadd'),
    path('project/', ProjectListView.as_view(), name='projects'),
    path('project/add/', ProjectAddView.as_view(), name='projectsadd'),

    # path('',taskpage),
]