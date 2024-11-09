from rest_framework import serializers
from apps.links.models import Link

class LinkSerializer(serializers.ModelSerializer):
    url_generate = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ['id_generate', 'user', 'product', 'title', 'created_at', 'url_generate']
        read_only_fields = ['id_generate', 'created_at', 'url_generate', 'user']

    def get_url_generate(self, obj):
        return obj.url_generate()

    # def validate(self, data):
    #     # Check if the user has the 'admin' role
    #     user = self.context['request'].user
    #     if not user.is_authenticated or not user.role == 'admin':
    #         raise ValidationError("Only admin users can create links.")
    #     return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
