from rest_framework import serializers
from apps.products.models.product_image import ProductImage  # Assuming the ProductImage model is here
from apps.products.models.products import Product

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']  # Adjust this if you want to include more fields

class ProductSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()  # Use SerializerMethodField for images

    class Meta:
        model = Product
        fields = [
            'id', 'main_category', 'sub_category', 'id_generate', 'name', 'price',
            'description', 'video_url', 'in_stock', 'admin_money', 'delivery_price',
            'is_active', 'like_counts', 'view_counts', 'comment_counts',
            'created_at', 'updated_at', 'features', 'images',
        ]

    def get_features(self, obj):
        return obj.get_features()

    def get_images(self, obj):
        # Call get_images method and serialize the result
        images = obj.get_images()  # This returns the related ProductImage queryset
        return ProductImageSerializer(images, many=True).data  # Serialize and return the data
