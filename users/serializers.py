from rest_framework import serializers
from users.models import User,Roles,Department,Positions,Company


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'email','first_name','last_name','password','phone_number','telegram_id','is_active','is_superuser')

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['role_name','description']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_name','department_head','deactivate','objects','activate']
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id','company_name','director']
class PositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Positions
        fields = ['position_name']







