from rest_framework import serializers
from users.models import User,Roles,Department,Positions,Company
class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['role_name','description']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
            # ['id','department_name','department_head','deactivate','objects','activate']
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id','company_name','director']
class PositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Positions
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    position = PositionsSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'email','first_name',
                   'last_name','password','position','role_user','department','image',
                   'phone_number','telegram_id','status',
                   'is_active','is_superuser'
                   )
