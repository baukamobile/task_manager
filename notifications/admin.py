from django.contrib import admin
from notifications.models import Notification
# Register your models here.


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['notification_text','notification_type']
    list_filter = ['notification_type']


admin.site.register(Notification, NotificationAdmin)

