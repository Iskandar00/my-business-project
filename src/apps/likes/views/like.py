from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.likes.models.like import ProductLike
from apps.likes.serializers.like import ProductLikeSerializer



class ProductLikeToggleView(generics.CreateAPIView):
    queryset = ProductLike.objects.all()
    serializer_class = ProductLikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product')

        like = ProductLike.objects.filter(user=user, product_id=product_id).first()

        if like:
            like.delete()
            return Response({"message": "Product like removed."}, status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response({"message": "Product liked."}, status=status.HTTP_201_CREATED)
