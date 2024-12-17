from rest_framework import serializers

from apps.wishlists.models import Wishlist
from apps.products.serializers import ProductSerializer


class WishlistListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = Wishlist
        fields = "__all__"