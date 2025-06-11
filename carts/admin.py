from django.contrib import admin
from .models import Cart, CartItem
# from .models import CartItem
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ( 'cart_id', 'date_added')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('product__product_name',)  # Assuming Product has a field 'product_name'

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)