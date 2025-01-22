from django.db import transaction
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from apps.links.models import Link
from apps.orders.models import Order
from apps.products.models import Product


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('product_count', 'buyer_name', 'phone_number', 'area')

    @transaction.atomic
    def create(self, validated_data):
        link = None
        link_id = self.context['request'].query_params.get('link')
        product_id = self.context['request'].query_params.get('product')
        
        if link_id:
            link = get_object_or_404(Link, id_generate=link_id)
            
            validated_data['product'] = link.product

            link.user.estimated_balance += link.product.admin_money * validated_data['product_count']
            link.user.save()
            
        if product_id:
            validated_data['product'] = get_object_or_404(Product, id=product_id)

        Order.objects.create(**validated_data, link=link)
        return validated_data

class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'product_count', 'buyer_name', 'phone_number', 'area', 'status', 'product', 'order_date')