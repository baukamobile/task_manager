from rest_framework import serializers
from rest_framework import serializers
from news.models import *

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class NewsCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model= NewsComment
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'