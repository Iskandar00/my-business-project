from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.likes.models.dislike import ProductDislike
from apps.likes.serializers.dislike import ProductDislikeSerializer

class ProductDislikeToggleView(generics.CreateAPIView):
    queryset = ProductDislike.objects.all()
    serializer_class = ProductDislikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product')

        # Check if dislike already exists
        dislike = ProductDislike.objects.filter(user=user, product_id=product_id).first()

        if dislike:
            # If it exists, delete it (toggle off)
            dislike.delete()
            return Response({"message": "Product dislike removed."}, status=status.HTTP_204_NO_CONTENT)
        else:
            # If it doesn't exist, create a new dislike (toggle on)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response({"message": "Product disliked."}, status=status.HTTP_201_CREATED)
