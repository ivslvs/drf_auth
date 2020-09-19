from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class MyUserAdmin(UserAdmin):
    """Extended admin panel"""
    list_display = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'last_login',
                    'is_staff', 'is_active', 'is_superuser')
    search_fields = ('email',)
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('email', 'date_joined', 'last_login')

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


admin.site.register(User, MyUserAdmin)
