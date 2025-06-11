from django.contrib import admin
from .models import Product
from .models import Variation

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'product_slug': ('product_name',)}
    list_display = ('product_name', 'product_price', 'product_stock', 'product_available')

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active', 'variation_value')
    list_filter = ('product', 'variation_category', 'is_active')

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)