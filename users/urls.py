from django.urls import path,include
from users.views import index

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('',include('users.urls')),
    path('',index),
]
