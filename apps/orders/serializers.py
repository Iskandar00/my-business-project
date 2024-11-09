from rest_framework import serializers

from apps.links.models import Link
from apps.orders.models import Order
from rest_framework.exceptions import ValidationError


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('product_count', 'buyer_name', 'phone_number', 'area',)

    def validate(self, data):
        order = Order(**data)
        try:
            order.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return data

    def create(self, validated_data):
        product_id = self.context.get("product_id")
        if product_id is None:
            raise serializers.ValidationError("Product ID is required in the context.")

        link = Link.objects.filter(product__id_generate=product_id, user=validated_data.user)
        if not link.exists():
            raise serializers.ValidationError("No such link exists.")

        link_instance = link.first()
        link_instance.user.total_balance += link_instance.product.admin_money * validated_data['product_count']
        link_instance.user.save()

        order = Order.objects.create(**validated_data)
        order.clean()
        order.save()
        return order
