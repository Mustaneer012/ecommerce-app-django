from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'product_slug': ('product_name',)}
    list_display = ('product_name', 'product_price', 'product_stock', 'product_available')

# Register your models here.
admin.site.register(Product, ProductAdmin)
