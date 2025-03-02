from django.urls import path,include
from event_calendar.models import Event
from event_calendar.views import EventViewSet
from rest_framework.routers import DefaultRouter
routers=DefaultRouter()
routers.register(r'event',EventViewSet)

urlpatterns = [
    path('',include(routers.urls))
]