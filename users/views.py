from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from users.serializers import *
import datetime
from rest_framework.response import Response
import jwt
from django.contrib.auth import authenticate
from django.conf import settings
import logging
# from users.tasks import send_mail_message,send_mail_to_logged_user
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
logger = logging.getLogger('users')

class UserViewSet(ModelViewSet): #Если рлдбзователь адинTaskViewSet
    # permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
#Получение данные о авторизованного пользователя
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
def get_user_info(request): ##функция чтобы получить данные авторизованного пользователя
    print('Request headers: ',request.headers)
    return Response({
        "id": request.user.id,
        "email": request.user.email,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "phone_number":request.user.phone_number,
        "posiiton":request.user.position,
        "department": request.user.department,
        "company":request.user.company,
        "is_active":request.user.is_active,
        "is_superuser":request.user.is_superuser
    })
def get_tokens_for_user(user): #тестовая функция
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    return {
        'access': str(access_token),
        'refresh': str(refresh)
    }

# class RolesViewSet(ModelViewSet):
#     queryset = Roles.objects.all()
#     serializer_class = RolesSerializer

class PositionsViewSet(ModelViewSet):
    queryset = Positions.objects.all()
    serializer_class = PositionsSerializer
    # permission_classes = [AllowAny]

class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # permission_classes = [AllowAny]
class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    # permission_classes = [AllowAny]









