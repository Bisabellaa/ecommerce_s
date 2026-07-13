from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name','last_name', 'username', 'last_login','date_joined', 'is_active')
    list_display_links = ('email', 'first_name','last_name')
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ('groups', 'user_permissions')
    list_filter = ('is_active', 'is_staff', 'is_admin')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'username', 'phone_number')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_superadmin', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(Account, AccountAdmin)