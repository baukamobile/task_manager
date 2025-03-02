from rest_framework.viewsets import ModelViewSet
from event_calendar.models import Event
from event_calendar.serializers import *
# Create your views here.

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer