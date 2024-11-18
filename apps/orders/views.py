from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.links.models import Link
from apps.orders.serializers import OrderSerializer


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        link_id = request.query_params.get('link')
        product_id = request.query_params.get('product')
        if not link_id and not product_id:
            return redirect('https://chatgpt.com/')
        if link_id:
            link = get_object_or_404(Link, id_generate=link_id)
            product = link.product
        if product_id:
            pass
        return Response(
            {'id_generate': product.id_generate,
             'name': product.name,
             'price': product.price,
             'description': product.description,
             'video_url': product.video_url,
             'delivery_price': product.delivery_price,
             'like_counts': product.like_counts,
             'view_counts': product.view_counts,
             'comment_counts': product.comment_counts,
             })

    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(order, status=status.HTTP_201_CREATED)