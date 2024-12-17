from django.shortcuts import get_object_or_404

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from apps.products.models import Product
from apps.wishlists.models import Wishlist
from apps.wishlists.serializer import WishlistListSerializer


class WishlistCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        product_id = request.GET.get('product_id')
        if not product_id:
            raise ValidationError('product_id kelmadi')
        product = get_object_or_404(Product, id=product_id)
        obj, create = Wishlist.objects.get_or_create(user=request.user, product=product)
        if not create:
            obj.delete()
            return Response({'success': 'product delete in wishlist'})
        return Response({'success': 'product create in wishlist'})
    

class WishlistListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistListSerializer
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)