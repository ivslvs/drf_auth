from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import Client, CustomGroup
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin


class AccountAdmin(UserAdmin):
    """Override admin panel"""

    list_display = ('pk', 'email', 'first_name', 'last_name', 'date_joined', 'last_login',
                    'is_admin', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('email',)
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('email', 'date_joined', 'last_login')

    # поля на регистрации и изменения пользователя через админку
    # после переопределения модельки User, пропало поле 'Groups with permissions' где я могла бы добавить Менеджеров
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'passport_number', 'password1', 'password2'),
        }
         ),
    )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Client, AccountAdmin)

# это полуработающий вариант переопределения модели Group
# при создании группы в админке, появляется выпадающий список с юзерами для регистрации менеджеров с пермишенс,
# но юзеры в списке Managers with permissions не сохраняются, логику не писала, не уверена в правильности идеи
class GroupInline(admin.StackedInline):
    """Override Group model"""

    model = CustomGroup
    can_delete = False
    verbose_name_plural = 'Custom groups'


class GroupAdmin(BaseGroupAdmin):
    inlines = (GroupInline,)


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
