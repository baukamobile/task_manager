from django.urls import path,include
from news.models import News,NewsComment,Tag
from notifications.views import NotificationViewSet
from rest_framework.routers import DefaultRouter
routers=DefaultRouter()
routers.register(r'notifications',NotificationViewSet),

urlpatterns = [
    path('',include(routers.urls))
]