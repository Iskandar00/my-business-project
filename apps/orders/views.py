from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.orders.serializers import OrderSerializer


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        serializer = OrderSerializer(data=request.data, context={"product_id": product_id})
        if serializer.is_valid():
            order = serializer.save()
            return Response(
                {"message": "Order created successfully!", "order_id": order.id},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
