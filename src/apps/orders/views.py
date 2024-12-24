from django.db.models import Sum
from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.links.models import Link
from apps.products.models.products import Product
from apps.products.serializers import ProductSerializer
from apps.orders.models import Order
from apps.orders.serializers import OrderListSerializer, OrderSerializer
from apps.orders.permissions import IsOperatorPermission
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
    permission_classes = [IsAuthenticated, IsOperatorPermission]
    
    def get(self, request):
        operator_orders = request.user.operator_orders.all()
        all_orders_with_operator = Order.objects.filter(operator__isnull=True)
        all_orders = Order.objects.all()

        operator_serializer = OrderListSerializer(operator_orders, many=True)
        all_orders_serializer = OrderListSerializer(all_orders_with_operator, many=True)
        all_orders = OrderListSerializer(all_orders, many=True)

        return Response({
            "operator_orders": operator_serializer.data,
            "all_orders_with_operator": all_orders_serializer.data,
            "all_orders": all_orders.data
        })


class AssignOperatorView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsOperatorPermission]
    serializer_class = None
    queryset = []

    def get(self, request, order_id):
        user = request.user
        order = get_object_or_404(Order, id=order_id)
        order.assign_operator(user_id=user.id)
        return Response({"detail": f"Siz {order_id} buyurtma uchun operator tayinladingiz {user.fullname}"},
                        status=status.HTTP_200_OK)

class DashboardStatistic(APIView):

    def get(self, request):
        stats = {
            "total_orders": Order.objects.aggregate(total=Sum('product_count'))["total"] or 0,
            "status_statistics": {
                status[1]: Order.objects.filter(status=status[0]).aggregate(total=Sum('product_count'))["total"] or 0
                for status in Order.StatusChoices.choices
            }
        }

        all_orders = Order.objects.all()
        serialized_orders = OrderListSerializer(all_orders, many=True)

        return Response({
            "statistics": stats,
            "all_orders": serialized_orders.data
        })