from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'date_joined', 'last_login', 'is_admin')
    readonly_fields = ('last_login', 'date_joined', 'password')
    list_display_links = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ('is_admin', 'is_staff', 'is_active', 'is_superadmin')
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        return format_html('<img src="{}" style="width: 30px; border-radius: 50%;" />'.format(obj.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
        
    list_display = ('user', 'city', 'state', 'country', 'thumbnail')
    search_fields = ('user__email', 'user__username')
    list_filter = ('country',)
    fieldsets = (
        (None, {
            'fields': ('user', 'address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')
        }),
    )

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)