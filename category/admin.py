from django.contrib import admin
from .models import Category
from django.utils.html import format_html
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('cat_name',)}
    list_display = ('cat_name', 'slug', 'cat_image_preview')

    def cat_image_preview(self, obj):
        if obj.cat_image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover;" />', obj.cat_image.url)
        return "No Image"

admin.site.register(Category, CategoryAdmin)