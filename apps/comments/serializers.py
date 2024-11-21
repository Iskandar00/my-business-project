from rest_framework import serializers

from apps.comments.models import Comment
from apps.users.serializers import UserProfileSerializer


class CommentListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Comment
        fields = '__all__'
        


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Comment
        fields = '__all__'