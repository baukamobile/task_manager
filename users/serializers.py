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
    position = serializers.PrimaryKeyRelatedField(queryset=Positions.objects.all())
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    class Meta:
        model = User
        fields = ('id', 'email','first_name',
                   'last_name','password','position','role_user','department','image',
                   'phone_number','telegram_id','status','company',
                   'is_active','is_superuser'
                   )
    def to_reprsentation(self,instance):
        """Чтобы в ответе возвращались вложенные данные"""
        data = super().to_representation(instance)
        data['position'] = PositionsSerializer(instance.position).data
        data['department']= DepartmentSerializer(instance.department).data
        data['company']=CompanySerializer(instance.company).data
        return data
