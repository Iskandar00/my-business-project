from rest_framework import serializers
from apps.likes.models.dislike import ProductDislike

class ProductDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDislike
        fields = ['id', 'user', 'product']
