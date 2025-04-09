from django.urls import path,include
from users.views import (UserViewSet,
                         PositionsViewSet,
                         CompanyViewSet,DepartmentViewSet)
from users.authentication import (RegisterView,LoginView, LogoutView)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users',UserViewSet),
router.register(r'positions',PositionsViewSet),
# router.register(r'roles',RolesViewSet),
router.register(r'company',CompanyViewSet)
router.register(r'department',DepartmentViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('api/register/', RegisterView.as_view()),
    path('api/login/',LoginView.as_view()),
    path('api/logout/',LogoutView.as_view()),
]




