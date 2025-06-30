from django.contrib import admin
from .models import Order, OrderProduct, Payment
# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ('payment','product', 'quantity', 'product_price', 'ordered')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at')
    list_filter = ('is_ordered', 'status')
    search_fields = ('order_number', 'first_name', 'last_name', 'phone', 'email')
    list_per_page = 15
    inlines = [OrderProductInline]



admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Payment)