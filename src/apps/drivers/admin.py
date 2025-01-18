from django.contrib import admin

from apps.drivers.models import ProductDelivery


@admin.register(ProductDelivery)
class ProductDeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'delivery', 'order', 'status', 'product', 'product_count',
                    'created_at', 'updated_at')
    list_display_links = list_display

    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('delivery__username', 'order__id', 'product__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'product', 'product_count')
