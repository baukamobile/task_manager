from django.contrib import admin
from django.contrib.auth.models import User
from users.models import RolesUser, Positions, Company, Department

# Register your models here.

admin.site.register(RolesUser)
admin.site.register(Positions)
admin.site.register(Company)
admin.site.register(User)
admin.site.register(Department)
# admin.site.register(UserCustomManager)

from django.contrib.auth.admin import UserAdmin


# Here you have to import the User model from your app!
from users.models import User

#
@admin.register(User)
class MyUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'email', 'phone_number', 'telegram_id', 'first_name','last_name', 'is_active', 'is_superuser')
    search_fields = ('email', 'phone_number', 'name')
    list_filter = ('is_active', 'is_superuser',)
    ordering = ('email',)
    filter_horizontal = ()

    # Override the fieldsets to remove references to non-existent fields
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name','last_name', 'phone_number', 'telegram_id', 'date_of_birth', 'address', 'status', 'position', 'department', 'company', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_verified', 'on_vacation', 'is_superuser', 'is_owner')}),
        ('Important Dates', {'fields': ('date_joined',)}),
    )

    # Add fieldsets for adding users without first_name, last_name, and username
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2'),
        }),
    )


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'phone_number', 'name', 'email', 'is_active', 'is_superuser')  # Выводимые поля
#     search_fields = ('phone_number', 'name', 'email')
#
# admin.site.register(User, UserAdmin)


