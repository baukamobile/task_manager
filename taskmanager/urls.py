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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include,re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Импорт для django-debug-toolbar
if settings.DEBUG:
    import debug_toolbar
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', TemplateView.as_view(template_name="index.html")),
    path('users/', include('users.urls')),
    path('tasks/', include('tasks.urls')),
    path('chat/', include('chat.urls')),
    path('news/', include('news.urls')),
    path('reports/', include('reports.urls')),
    path('events/', include('event_calendar.urls')),
    path('notifications/', include('notifications.urls')),
    path('bpm/',include('bpm.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^(?!api/|static/|media/|assets/).*$', TemplateView.as_view(template_name='index.html'), name='spa'),
]

# Добавляем debug_toolbar, если DEBUG = True
if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

# Статические файлы
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Медиафайлы (только в DEBUG)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

