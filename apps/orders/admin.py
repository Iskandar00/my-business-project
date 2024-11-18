from django.contrib import admin
from apps.orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('admin', 'id', 'buyer_name', 'phone_number', 'area', 'status',
                    'product', 'product_count', 'total_balance',
                    'estimated_balance', 'order_date')
    list_display_links = list_display
    list_filter = ('admin', 'status', 'area', 'order_date')
    search_fields = ('buyer_name', 'phone_number', 'product__name', 'product__company')
    ordering = ('-order_date',)
    readonly_fields = ('id', 'order_date', 'total_balance', 'estimated_balance')
