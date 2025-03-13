from rest_framework import serializers
from users.serializers import UserSerializer
from news.models import *


class TagSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = Tag
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True,read_only=True)
    created_by = serializers.SerializerMethodField()
    class Meta:
        model = News
        fields = '__all__'
    def get_created_by(self,obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"

class NewsCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model= NewsComment
        fields = '__all__'


