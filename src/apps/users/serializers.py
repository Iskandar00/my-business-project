from rest_framework import serializers

from apps.users.models import CustomUser


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', "username", "fullname", "phone_number", "email"]