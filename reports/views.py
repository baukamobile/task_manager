from django.shortcuts import render
from reports.models import Reports
from rest_framework.viewsets import ModelViewSet
from reports.serializers import *

# Create your views here.

class ReportsViewSet(ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportSerializer

