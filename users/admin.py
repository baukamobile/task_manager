from django.contrib import admin
# from django.contrib.auth.models import User
from users.models import Roles, Positions, Company, Department
from users.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class GetEmployeesMixin:
    #функция чтобы вывести список сотрудников
    def get_employees(self,obj):
        return ', '.join([user.first_name for user in obj.employees.all()])
    get_employees.short_description = "Employee name"

class RolesAdmin(admin.ModelAdmin,GetEmployeesMixin):
    list_display = ['role_name','get_employees']
admin.site.register(Roles,RolesAdmin)
class PostitionAdmin(admin.ModelAdmin,GetEmployeesMixin):
    list_display = ['position_name','get_employees']

admin.site.register(Positions,PostitionAdmin)


# admin.site.register(User)

class DepartmentAdmin(admin.ModelAdmin,GetEmployeesMixin):
    list_display = ['department_name','department_head','get_employees']


class CompanyAdmin(admin.ModelAdmin,GetEmployeesMixin):
    list_display = ['company_name','director','has_admin','get_employees']

admin.site.register(Department,DepartmentAdmin)
admin.site.register(Company,CompanyAdmin)

@admin.register(User)
class MyUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'email', 'phone_number', 'company_id', 'first_name','last_name', 'is_active', 'is_superuser')
    search_fields = ('email', 'phone_number', 'name')
    list_filter = ('is_active', 'is_superuser',)
    ordering = ('email',)
    filter_horizontal = ()

    # Override the fieldsets to remove references to non-existent fields
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name','last_name', 'phone_number', 'telegram_id', 'date_of_birth', 'address', 'status', 'position','role_user', 'department', 'company', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_verified', 'on_vacation', 'is_superuser', 'is_owner')}),
        ('Important Dates', {'fields': ('date_joined',)}),
    )

    # необходимые поля чтобы добавить пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name','phone_number','telegram_id', 'password1', 'password2'),
        }),
    )


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'phone_number', 'name', 'email', 'is_active', 'is_superuser')  # Выводимые поля
#     search_fields = ('phone_number', 'name', 'email')
#
# admin.site.register(User, UserAdmin)


