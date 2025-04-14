from django.urls import path,include
from rest_framework.routers import DefaultRouter
from bpm.views import *
router = DefaultRouter()
router.register(r'process',ProcessViewSet),
# router.register(r'workflow',WorkflowStepViewSet),
router.register(r'process-template',ProcessTemplateViewSet),
router.register(r'process-stage-template',ProcessStageTemplateViewSet),
router.register(r'process-stage',ProcessStageViewSet),
router.register(r'task',TaskViewSet),
router.register(r'task-stage-history',TaskStageHistoryViewSet),
router.register(r'auto-task-rule',AutoTaskRuleViewSet),
router.register(r'attachment',AttachmentViewSet),
router.register(r'comment',CommentViewSet),
router.register(r'notification',NotificationViewSet),
# router.register(r'user-department-role',UserDepartmentRoleViewSet),
router.register(r'dashboard',DashboardViewSet),
router.register(r'dashboard-widget',DashboardWidgetViewSet),
router.register(r'process-element',ProcessElementViewSet),
router.register(r'element-connection',ElementConnectionViewSet),
router.register(r'process-execution',ProcessExecutionViewSet)

# admin.site.register(WorkflowStep)

urlpatterns = [
    path('',include(router.urls)),
]
