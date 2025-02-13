from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email','first_name','last_name','password','phone_number','telegram_id','is_active','is_superuser')









