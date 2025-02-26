from django.contrib import admin
from event_calendar.models import *
# Register your models here.



class EventAdmin(admin.ModelAdmin):
    list_display = ['event_type','start_date','end_date','description']
    list_filter = ['event_type','start_date','end_date']
admin.site.register(Event,EventAdmin)
