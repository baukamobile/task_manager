from django.urls import path,include
from rest_framework.routers import DefaultRouter
from reports.views import ReportsViewSet
routers = DefaultRouter()
routers.register(r'reports',ReportsViewSet)


urlpatterns = [
    path('',include(routers.urls))
]