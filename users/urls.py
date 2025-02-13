from django.urls import path,include
from users.views import index, UserList

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('',include('users.urls')),
    path('',index),
    path('api/users/', UserList.as_view()),
]
