from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from tasks.models import *
from users.serializers import *
import datetime
from rest_framework.response import Response



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


class register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class loginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email = email).first()


        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=90),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()

        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data ={
            'jwt':token
        }

        return response


class userget(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('unauthenticated')

        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')

        user = CustomUser.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)

class logoutView(APIView):
    def post(self,request):
        respnse = Response()
        respnse.delete_cookie('jwt')
        respnse.data = {
            "message":"success"
        }
        return respnse


