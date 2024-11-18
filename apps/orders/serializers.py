from django.db import transaction
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from apps.links.models import Link
from apps.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('product_count', 'buyer_name', 'phone_number', 'area',)

    @transaction.atomic
    def create(self, validated_data):
        link_id = self.context['request'].query_params.get('link')
        link = get_object_or_404(Link, id_generate=link_id)

        link.user.estimated_balance += link.product.admin_money * validated_data['product_count']
        link.user.save()

        Order.objects.create(**validated_data, link=link)
        return validated_data
