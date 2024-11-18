from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.comments.serializers import CommentCreateSerializer, CommentListSerializer
from apps.comments.models import Comment

class CommentCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentCreateSerializer
    queryset = []
    
    
class CommentListAPIView(GenericAPIView):
    serializer_class = CommentListSerializer
    queryset = Comment.objects.all()
    
    def get(self, request, product_id, *args, **kwargs):
        comments = Comment.objects.filter(product_id=product_id)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)