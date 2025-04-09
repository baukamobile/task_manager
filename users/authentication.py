from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
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
from users.models import User
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
        refresh = RefreshToken.for_user(user)
        # send_mail_message.delay(user.id)  # фоновая задача отправки сообщение на эмайл нового ползователя
        #Возвращаем даааные вместе с токенами
        return Response({
            'user': UserSerializer(user).data,
            'jwt': str(refresh.access_token),
            'refresh': str(refresh)
        })



class LoginView(APIView):
    def post(self, request):
        logger.info("Пользователь пытается войти")
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            logger.warning("Попытка входа без почты и пароля")
            raise AuthenticationFailed('Email and password are required')

        user = authenticate(username=email, password=password)
        if user is None:
            logger.warning(f'Неудачный вход {email} неверные данные')
            raise AuthenticationFailed('Invalid credentials')

        # Создаем токен с помощью simplejwt
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        logger.info(f'Пользователь {user.email} успешно вошел на сайт')

        # Отправляем ответ с токенами
        return Response({
            'access': access_token,
            'refresh': str(refresh)
        })



class LogoutView(APIView):
    def post(self,request):

        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist() #чтобы token больше не работали, даже если ещё живы по сроку.
            logger.info('Пользователь вышел из системы')
            return Response({
                'message': 'Success'
            },status=200)
        except Exception as e:
            logger('Ошибка при выходе из аккаунта: ',str(e))
            return Response({f'error: ', str(e)}, status=401)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,

        })







