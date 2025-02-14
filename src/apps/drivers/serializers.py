from rest_framework import serializers
from .models import ProductDelivery

class ProductDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDelivery
        fields = ('id', 'delivery', 'order', 'status', 'product', 'product_count', 'created_at', 'updated_at',)
        read_only_fields = ('product', 'product_count', 'created_at', 'updated_at')

    def validate(self, attrs):
        if attrs.get('order') is None:
            raise serializers.ValidationError("Order field is required.")
        if attrs.get('status') not in [choice[0] for choice in ProductDelivery.Status.choices]:
            raise serializers.ValidationError("Invalid status value.")
        return attrs
