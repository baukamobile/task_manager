from notifications.models import Notification
from rest_framework.viewsets import ModelViewSet
from notifications.serializers import *
import logging
logger = logging.getLogger('reports')
# Create your views here.
class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    # logger.info('получение список reports')

from django.utils.translation import gettext_lazy as _




