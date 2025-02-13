from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from tasks.models import *
from users.serializers import *
import datetime
from rest_framework.response import Response
import jwt
from django.contrib.auth import authenticate
from django.conf import settings



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


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(**serializer.validated_data)

        return Response(UserSerializer(user).data)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            raise AuthenticationFailed('Email and password are required')

        user = authenticate(username=email, password=password)
        if user is None:
            raise AuthenticationFailed('Invalid credentials')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=90),
            'iat': datetime.datetime.utcnow()
        }

        SECRET = getattr(settings, 'JWT_SECRET_KEY', settings.SECRET_KEY)
        token = jwt.encode(payload, SECRET, algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}

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

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)

class LogoutView(APIView):
    def post(self,request):
        respnse = Response()
        respnse.delete_cookie('jwt')
        respnse.data = {
            "message":"success"
        }
        return respnse


