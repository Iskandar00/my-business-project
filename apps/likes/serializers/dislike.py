from rest_framework import serializers
from apps.likes.models.dislike import ProductDislike

class ProductDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDislike
        fields = ['id', 'user', 'product']
        read_only_fields = ['user']  # Make the 'user' field read-only

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            # Assign the user from the request to the validated data
            validated_data['user'] = request.user
        return super().create(validated_data)
