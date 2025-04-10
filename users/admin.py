from django.contrib import admin
from django.utils.safestring import mark_safe
import logging
# from django.contrib.auth.models import User
from users.models import Positions, Company, Department #Roles,
from tasks.models import Task,Projects,Priority,Task_comments,Status
from bpm.models import (Process,ProcessTemplate,ProcessStageTemplate,ProcessStage,
                        Task as bpmTask,TaskStageHistory,AutoTaskRule,Attachment,
                        Comment,Notification,Dashboard,DashboardWidget)
from users.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Department  # Импортируем модель, для которой получаем права
#Создание групп (ролей)
logger = logging.getLogger('users')

admin_group, _ = Group.objects.get_or_create(name="Admin")
department_head_group, _ = Group.objects.get_or_create(name="Department Head") #_ — это заглушка для второго значения (того самого True/False), которое нам все равно потому что мы не исползуем true false
director_group, _ = Group.objects.get_or_create(name="Director")
employee_group, _ = Group.objects.get_or_create(name="Employee")
# Создаём или получаем группу
# Получаем ContentType для модели Department

#Общий модел из одного приложение
# Получаем все ContentType для моделей из приложения bpm
bpm_model_type = ContentType.objects.filter(app_label='bpm')
user_model_type = ContentType.objects.filter(app_label='users')
# Получаем все права для моделей из приложении
bpm_permissions = Permission.objects.filter(content_type__in=bpm_model_type)
user_permissions = Permission.objects.filter(content_type__in=user_model_type)

# Берем ContentType для моделей
department_content_type = ContentType.objects.get_for_model(Department)
users_content_type = ContentType.objects.get_for_model(User)
company_content_type = ContentType.objects.get_for_model(Company)
# roles_content_type = ContentType.objects.get_for_model(Roles)
bpm_task_content_type = ContentType.objects.get_for_model(bpmTask)
# Вытаскиваем права для каждой модели
department_permissions = Permission.objects.filter(content_type=department_content_type)
# users_permissions = Permission.objects.filter(content_type=users_content_type)
company_permissions = Permission.objects.filter(content_type=company_content_type)
# roles_permissions = Permission.objects.filter(content_type=roles_content_type)
bpm_task_permissions = Permission.objects.filter(content_type=bpm_task_content_type)
# Пихаем все права в группу
admin_group.permissions.add(
    *department_permissions,
    *user_permissions,
    *company_permissions,
    # *roles_permissions,
    *bpm_permissions
)
director_group.permissions.add(
*department_permissions,
    *user_permissions,
    # *roles_permissions,
    *bpm_task_permissions
)
# logger.warning(f'Ползователь {admin_group.name} Права добавлены в группу')
# Проверяем, добавлены ли права
# print(f"Права добавлены в группу '{admin_group.name}'")



# Добавление прав к группам




class GetEmployeesMixin:
    #функция чтобы вывести список сотрудников
    def get_employees(self,obj):
        return ', '.join([user.first_name for user in obj.employees.all()])
    get_employees.short_description = "Employee name"

# class RolesAdmin(admin.ModelAdmin,GetEmployeesMixin):
#     list_display = ['role_name',]
#     filter_horizontal = ('permissions',)

# admin.site.register(Roles,RolesAdmin)
class PostitionAdmin(admin.ModelAdmin,GetEmployeesMixin):
    list_display = ['position_name']

admin.site.register(Positions,PostitionAdmin)


# admin.site.register(User)

class DepartmentAdmin(admin.ModelAdmin,GetEmployeesMixin):
    list_display = ('department_name','department_head')
    list_filter = ('department_with_access',)


class CompanyAdmin(admin.ModelAdmin,GetEmployeesMixin):
    list_display = ['company_name','director']

admin.site.register(Department,DepartmentAdmin)
admin.site.register(Company,CompanyAdmin)

@admin.register(User)
class MyUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'email','first_name','last_name','position', 'phone_number', 'company','department','address','date_of_birth', 'is_active', 'is_superuser')
    search_fields = ('email', 'phone_number', 'name')
    list_filter = ('is_active', 'is_superuser','company','department','date_of_birth') #'role_user',
    ordering = ('email',)
    filter_horizontal = ()

    # Override the fieldsets to remove references to non-existent fields
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name','last_name', 'phone_number', 'telegram_id', 'date_of_birth', 'address', 'status', 'position', 'department', 'company', 'image')}), #'role_user',
        ('Permissions', {'fields': ('is_active', 'is_verified', 'on_vacation', 'is_superuser')}),
        ('Important Dates', {'fields': ('date_joined',)}),
    )

    # необходимые поля чтобы добавить пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name','phone_number','telegram_id', 'password1', 'password2'),
        }),
    )


