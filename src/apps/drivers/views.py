from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ProductDelivery
from .serializers import ProductDeliverySerializer


class ProductDeliveryListCreateView(generics.ListCreateAPIView):

    queryset = ProductDelivery.objects.all()
    serializer_class = ProductDeliverySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class ProductDeliveryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductDelivery.objects.all()
    serializer_class = ProductDeliverySerializer
    permission_classes = [IsAuthenticated]
