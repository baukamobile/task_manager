from django.shortcuts import render
from news.models import *
from rest_framework.viewsets import ModelViewSet
from news.serializers import *
# Create your views here.
import logging
logger = logging.getLogger('news')

class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # logger.info('получение список news')

class NewsCommentViewSet(ModelViewSet):
    queryset = NewsComment.objects.all()
    serializer_class = NewsCommentSerializer
    # logger.info('получение список news commnets')


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # logger.info('получение список news tags')