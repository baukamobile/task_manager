from django.contrib import admin
from chat.models import *

# Register your models here.


admin.site.register(Chat)
admin.site.register(MessageHistory)
admin.site.register(Messages)



