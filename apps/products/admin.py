from django.contrib import admin
from apps.products.models.products import Product
from apps.products.models.product_image import ProductImage
from apps.products.models import ProductFeature


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5
    select_related = ('product',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'price', 'in_stock', 'is_active', 'like_counts', 'view_counts', 'comment_counts', 'created_at'
    )
    list_display_links = list_display
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'id_generate')
    ordering = ('-created_at',)
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'ordering_number')
    list_display_links = list_display
    list_filter = ('product',)
    search_fields = ('product__name',)
    ordering = ('ordering_number',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('product')


@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'feature_value')
    list_filter = ('product',)
    search_fields = ('product__name', 'feature_value__value')

    def get_queryset(self, request):
        """
        Use `select_related` to fetch related fields in a single query.
        """
        queryset = super().get_queryset(request)
        return queryset.select_related('product', 'feature_value')
