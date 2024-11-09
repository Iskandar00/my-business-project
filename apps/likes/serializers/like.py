from rest_framework import serializers
from apps.likes.models.like import ProductLike

class ProductLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLike
        fields = ['id', 'user', 'product']
