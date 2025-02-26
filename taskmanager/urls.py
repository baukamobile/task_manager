"""
URL configuration for taskmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import logging
logger = logging.getLogger('admin')
# from jet.dashboard.dashboard_modules import google_analytics_views
urlpatterns = [

    # path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    # path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),


    path('users/',include('users.urls')),
    # path("", include('admin_berry.urls')),
    path('tasks/',include('tasks.urls')),
    path('chat/',include('chat.urls')),
    path('news/',include('news.urls')),
    path('reports/',include('reports.urls')),
    path('notifications/',include('notifications.urls')),

]

