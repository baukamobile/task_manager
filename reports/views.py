from django.shortcuts import render
from reports.models import Reports
from rest_framework.viewsets import ModelViewSet
from reports.serializers import *
from users.models import User
from django.http import HttpResponse
import csv
# Create your views here.
#создание текстоый файл для отчетов
def report_user_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=report_about_users.txt'
    # users = User.objects.all()
    lines = ['This is line 1\n',
             'This is line 2\n',
             'This is line 3\n',
             ]
    response.writelines(lines)
    return response


class ReportsViewSet(ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportSerializer

# def report_user_csv(request)



