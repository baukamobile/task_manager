
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from bpm.views import *
from bpm.bpmn_parser import *
router = DefaultRouter()
router.register(r'process',ProcessViewSet),

router.register(r'xml-process',BpmXmlProcessViewSet),
router.register(r'attachment',AttachmentViewSet),

router.register(r'notification',NotificationViewSet),
router.register(r'task',TaskViewSet),
router.register(r'process-element',ProcessElementViewSet),


urlpatterns = [
    path('',include(router.urls)),
    path('process/<int:pk>/update-xml/',ProcessUpdateXmlView.as_view())
]
