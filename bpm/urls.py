from django.urls import path,include
from rest_framework.routers import DefaultRouter
from bpm.views import *
router = DefaultRouter()
router.register(r'process',ProcessViewSet),
router.register(r'workflow',WorkflowStepViewSet),

urlpatterns = [
    path('',include(router.urls)),
]
