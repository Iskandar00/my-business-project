from rest_framework import serializers
from apps.links.models import Link
from rest_framework.exceptions import ValidationError

from apps.users.models import CustomUser


class LinkSerializer(serializers.ModelSerializer):
    url_generate = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Link
        fields = ['id_generate', 'user', 'product', 'title', 'created_at', 'url_generate']
        read_only_fields = ['id_generate', 'created_at', 'url_generate', 'user']

    def get_url_generate(self, obj):
        return obj.url_generate()

    def validate(self, data):
        user = self.context['request'].user
        if user.role != CustomUser.RoleChoices.Admin.value:
            raise ValidationError("Only admin users can create links.")
        return data