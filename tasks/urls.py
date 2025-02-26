from django.urls import path

from tasks.views import TaskListView, taskpage, StatusListView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='tasks'),
    path('status/', StatusListView.as_view(), name='status'),
    path('',taskpage),
]