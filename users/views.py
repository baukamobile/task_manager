from django.shortcuts import render

from users.models import *
from tasks.models import *
from news.models import *


# Create your views here.
def index(request):
    users = User.objects.all()
    departments = Department.objects.all()
    tasks = Task.objects.all()
    return render(request,'index.html',context={
        'users':users,
        'departments':departments,
        'tasks':tasks,})