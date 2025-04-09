from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from users.serializers import *
import datetime
from rest_framework.response import Response
import jwt
from django.contrib.auth import authenticate
from django.conf import settings
import logging
from users.tasks import send_mail_message,send_mail_to_logged_user

logger = logging.getLogger('users')



class RegisterView(APIView):
    def post(self, request):
        logger.info("Ползователь пытается пройти регистрацию")
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            logger.warning(f"Ошибка валидации данных: {serializer.errors}")
            return Response(serializer.errors, status=400)
        # user = User.objects.create_user(**serializer.validated_data)
        user = User.objects.create_user(
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data.get('first_name', ''),
            last_name=serializer.validated_data.get('last_name', ''),
            password=serializer.validated_data['password'],
            phone_number=serializer.validated_data['phone_number'],  #  Теперь передается
            position =serializer.validated_data['position'],
            department=serializer.validated_data['department'],
            company=serializer.validated_data['company'],
            telegram_id=serializer.validated_data.get('telegram_id'),
            is_active=serializer.validated_data.get('is_active', True),
            is_superuser=serializer.validated_data.get('is_superuser', False),
        )
        logger.info(f'Ползователь {user.email} прошел регистрацию успешно')

        send_mail_message.delay(user.id)  # фоновая задача отправки сообщение на эмайл нового ползователя
        return Response(UserSerializer(user).data)



class LoginView(APIView):
    def post(self, request):
        logger.info("Ползователь пытается войти")
        # print('Ползователь пытается войти')
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            logger.warning("Попытка входа без почты и пароля")
            # print("Попытка входа без почты и пароля")
            raise AuthenticationFailed('Email and password are required')

        user = authenticate(username=email, password=password)
        if user is None:
            logger.warning(f'Неудачный вход {user.email} неверные данные')
            # print(f'Неудачный вход {user.email} неверные данные')
            raise AuthenticationFailed('Invalid credentials')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=90),
            'iat': datetime.datetime.utcnow()
        }

        SECRET = getattr(settings, 'JWT_SECRET_KEY', settings.SECRET_KEY)
        token = jwt.encode(payload, SECRET, algorithm='HS256')
        logger.info(f'Ползователь с {user.email} вошел на сайт {user.id}')
        # print(f'Ползователь с {user.email} паролем {user.password} вошел на сайт {user.id}')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}
        logger.info(f'Ползователь с {user.email} вошел на сайт {user.id}')
        print(f'Ползователь с {user.email} вошел на сайт {user.id}')
        # periodic_send_mail.delay(user.id) # фоновая задача периодический отправки сообщение на эмайл нового ползователя
        send_mail_to_logged_user.delay(user.id)
        return response



class LogoutView(APIView):
    def post(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            logger.warning('Пытается выйти без токена')
            return Response({'error':'unauthenticated'}, status=401)
        logger.info('Пользователь вышел из системы')

        respnse = Response()
        respnse.delete_cookie('jwt')
        respnse.data = {
            "message":"success"
        }
        return reponse











