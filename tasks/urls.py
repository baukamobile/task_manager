from django.urls import path
from rest_framework.routers import DefaultRouter
from tasks.views import TaskListView, taskpage, StatusListView,TaskDetailView,StatusDetailView
router = DefaultRouter()
# router.register(r'status',StatusListView),
# router.register(r'tasks',TaskListView),
urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='tasks'),
    path('status/', StatusListView.as_view(), name='status'),
    path('status/<int:pk>/', StatusDetailView.as_view(), name='status'),

    path('',taskpage),
]