from django.shortcuts import render
from news.models import *
from rest_framework.viewsets import ModelViewSet
from news.serializers import *
# Create your views here.


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class NewsCommentViewSet(ModelViewSet):
    queryset = NewsComment.objects.all()
    serializer_class = NewsCommentSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer