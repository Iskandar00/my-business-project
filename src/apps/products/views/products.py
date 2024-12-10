from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.products.models.products import Product
from apps.products.serializers.products import ProductSerializer


class ProductListView(APIView):
    """
    View to list all products.
    """

    def get(self, request):
        products = Product.objects.all().prefetch_related("product_images")
        serializer = ProductSerializer(products, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
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
