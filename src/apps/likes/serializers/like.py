from rest_framework import serializers
from apps.likes.models.like import ProductLike

class ProductLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLike
        fields = ['id', 'user', 'product']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['user'] = request.user
        return super().create(validated_data)
