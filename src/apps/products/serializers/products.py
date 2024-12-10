from django.conf import settings

from rest_framework import serializers

from apps.products.models.product_image import ProductImage  # Assuming the ProductImage model is here
from apps.products.models.products import Product



class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image']

    def get_image(self, obj):
        print('asdasd')
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return f"{settings.MEDIA_URL}{obj.image}" 


class ProductSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()
    product_images = ProductImageSerializer(many=True, read_only=True)  # Use SerializerMethodField for images

    class Meta:
        model = Product
        fields = [
            'id', 'main_category', 'sub_category', 'id_generate', 'name', 'price',
            'description', 'video_url', 'in_stock', 'admin_money', 'delivery_price',
            'is_active', 'like_counts', 'view_counts', 'comment_counts',
            'created_at', 'updated_at', 'features', 'product_images',
        ]

    def get_features(self, obj):
        return obj.get_features()