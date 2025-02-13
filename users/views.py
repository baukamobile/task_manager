from django.shortcuts import render
from rest_framework.generics import ListAPIView
from tasks.models import *
from users.serializers import *



def index(request):
    users = User.objects.all()
    departments = Department.objects.all()
    tasks = Task.objects.all()
    return render(request,'index.html',context={
        'users':users,
        'departments':departments,
        'tasks':tasks,})

class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


