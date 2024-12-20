from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.links.models import Link
from apps.orders.serializers import OrderSerializer
from apps.products.models.products import Product
from apps.products.serializers import ProductSerializer

from apps.orders.serializers import OrderListSerializer

from apps.orders.models import Order
from rest_framework.views import APIView


class CreateOrderView(GenericAPIView):
    serializer_class = OrderSerializer
    queryset = []

    def get(self, request):
        link_id = request.query_params.get('link')
        product_id = request.query_params.get('product')
        if not link_id and not product_id:
            return Response({'error': 'link and product not found'}, status=404)
        if link_id:
            link = get_object_or_404(Link.objects.select_related('product'), id_generate=link_id)
            product = link.product
        if product_id:
            product = get_object_or_404(Product, id=product_id)
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
             'features': product.get_features(),
             'images': ProductSerializer(product).data['product_images'],
             })

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderListView(GenericAPIView):
    def get(self, request):
        operator_orders = request.user.operator_orders.all()
        all_orders = Order.objects.all()

        operator_serializer = OrderListSerializer(operator_orders, many=True)
        all_orders_serializer = OrderListSerializer(all_orders, many=True)

        return Response({
            "operator_orders": operator_serializer.data,
            "all_orders": all_orders_serializer.data,
        })




class AssignOperatorView(APIView):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        try:
            user = request.user.id
            order.assign_operator(user_id=user)
            return Response({"detail": f"Siz {order_id} buyurtma uchun operator tayinladingiz {user}"},
                            status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
