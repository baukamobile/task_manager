from rest_framework import serializers
from users.models import User,Roles,Department,Positions,Company
class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['role_name','description']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id','department_name','department_head','deactivate','objects','activate']
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id','company_name','director']
class PositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Positions
        fields = ['id','position_name']

class UserSerializer(serializers.ModelSerializer):
    position = PositionsSerializer()
    department = DepartmentSerializer()
    class Meta:
        model = User
        fields = ('id', 'email','first_name',
                   'last_name','password','position','role_user','department','image',
                   'phone_number','telegram_id',
                   'is_active','is_superuser'
                   )
# class TagSerializer(serializers.ModelSerializer):
#     tags = serializers.SlugRelatedField(
#         many=True,
#         slug_field='name',
#         read_only=True
#     )
#
#     class Meta:
#         model = Tag
#         fields = '__all__'
#
# class NewsSerializer(serializers.ModelSerializer):
#     tags = TagSerializer(many=True,read_only=True)
#     created_by = serializers.SerializerMethodField()
#     class Meta:
#         model = News
#         fields = '__all__'
#     def get_created_by(self,obj):
#         return f"{obj.created_by.first_name} {obj.created_by.last_name}"

