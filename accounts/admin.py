from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'date_joined', 'last_login', 'is_admin')
    readonly_fields = ('last_login', 'date_joined', 'password')
    list_display_links = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ('is_admin', 'is_staff', 'is_active', 'is_superadmin')
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
