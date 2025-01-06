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
from apps.likes.models import ProductLike, ProductDislike


class CreateOrderView(GenericAPIView):
    serializer_class = OrderSerializer

    def get(self, request):
        link_id = request.query_params.get('link')
        product_id = request.query_params.get('product')

        if not link_id and not product_id:
            return Response({'error': 'Both link and product parameters are missing.'}, status=400)


        if link_id:
            link = get_object_or_404(Link.objects.select_related('product'), id_generate=link_id)
            product = link.product
            product_like_count = ProductLike.objects.filter(product_id=product.id).select_related('user', 'product').count()
            product_dislike_count = ProductDislike.objects.filter(product_id=product.id).select_related('user', 'product').count()

        if product_id:
            product = get_object_or_404(Product, id=product_id)
            product_like_count = ProductLike.objects.filter(product_id=product.id).select_related('user', 'product').count()
            product_dislike_count = ProductDislike.objects.filter(product_id=product.id).select_related('user', 'product').count()

        if not product:
            return Response({'error': 'Product not found.'}, status=404)

        product_data = {
            'id_generate': product.id_generate,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'video_url': product.video_url,
            'delivery_price': product.delivery_price,
            'like_counts': product.like_counts,
            'view_counts': product.view_counts,
            'comment_counts': product.comment_counts,
            'features': product.get_features(),
            'images': ProductSerializer(product).data.get('product_images', []),
            'product_like_count': product_like_count,
            'product_dislike_count': product_dislike_count,
        }

        return Response(product_data, status=200)

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OperatorOrdersView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsOperatorPermission]

    def get(self, request):
        operator_orders = request.user.operator_orders.all()
        serializer = OrderListSerializer(operator_orders, many=True)
        return Response({"operator_orders": serializer.data})


class AllOrdersWithOperatorView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsOperatorPermission]

    def get(self, request):
        all_orders_with_operator = Order.objects.filter(operator__isnull=True)
        serializer = OrderListSerializer(all_orders_with_operator, many=True)
        return Response({"all_orders_with_operator": serializer.data})


class AllOrdersView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsOperatorPermission]

    def get(self, request):
        all_orders = Order.objects.all()
        serializer = OrderListSerializer(all_orders, many=True)
        return Response({"all_orders": serializer.data})

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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == user.RoleChoices.Admin:
            user_orders = Order.objects.filter(admin=user)
        elif user.role == user.RoleChoices.Operator:
            user_orders = Order.objects.filter(operator=user)
        elif user.role == user.RoleChoices.Director:
            user_orders = Order.objects.all()
        else:
            return Response({"detail": "You do not have permission to view order statistics."}, status=403)

        stats = {
            "total_orders": user_orders.aggregate(total=Sum('product_count'))["total"] or 0,
            "status_statistics": {
                status[1]: user_orders.filter(status=status[0]).aggregate(total=Sum('product_count'))["total"] or 0
                for status in Order.StatusChoices.choices
            }
        }

        serialized_orders = OrderListSerializer(user_orders, many=True)

        return Response({
            "statistics": stats,
            "all_orders": serialized_orders.data
        })