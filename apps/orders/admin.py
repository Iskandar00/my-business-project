from django.contrib import admin
from apps.orders.models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer_name', 'phone_number', 'area', 'status', 'product', 'product_count', 'admin_money', 'order_date')
    list_display_links = list_display
    list_filter = ('status', 'area', 'order_date')
    search_fields = ('buyer_name', 'phone_number', 'product__name', 'product__company')
    ordering = ('-order_date',)
    readonly_fields = ('id', 'order_date', 'admin_money')


