from django.urls import path

from tasks.views import TaskListView,taskpage

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='tasks'),
    path('',taskpage),
]