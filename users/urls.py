from django.urls import path,include
from users.views import index, UserList, RegisterView, LoginView, LogoutView,basepage

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('',include('users.urls')),
    path('',index),
    path('base/',basepage),
    path('api/users/', UserList.as_view()),
    path('api/register/', RegisterView.as_view()),
    path('api/login/',LoginView.as_view()),
    path('api/logout/',LogoutView.as_view()),
]






