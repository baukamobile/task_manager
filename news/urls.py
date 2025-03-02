from django.urls import path,include
from news.models import News,NewsComment,Tag
from news.views import NewsViewSet,NewsCommentViewSet,TagViewSet
from rest_framework.routers import DefaultRouter
routers=DefaultRouter()
routers.register(r'news',NewsViewSet),
routers.register(r'newscomments',NewsCommentViewSet),
routers.register(r'tags',TagViewSet)


urlpatterns = [
    path('',include(routers.urls))
]