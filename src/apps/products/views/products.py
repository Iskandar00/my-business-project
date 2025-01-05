from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from apps.products.models.products import Product
from apps.products.serializers.products import ProductSerializer


class ProductListAPIView(ListAPIView):
    """
    View to list all products.
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all().prefetch_related("product_images")


class ProductDetailAPIView(APIView):
    """
    View to retrieve a single product by ID.
    """

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
