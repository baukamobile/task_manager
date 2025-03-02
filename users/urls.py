from django.urls import path,include
from users.views import UserViewSet, RegisterView, LoginView, LogoutView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users',UserViewSet)
urlpatterns = [
    path('',include(router.urls)),
    # router.register(r'status',UserViewSet),
    # path('admin/', admin.site.urls),
    # path('',include('users.urls')),
    # path('',index),
    # path('api/users/', UserList.as_view()),
    path('api/register/', RegisterView.as_view()),
    path('api/login/',LoginView.as_view()),
    path('api/logout/',LogoutView.as_view()),
]






