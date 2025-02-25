from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache

from rest_framework import serializers

from apps.authentication.utils import generate_jwt_tokens
from apps.users.sms_providers import EskizUz
from apps.users.validators import phone_validate


class SendCodeSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[phone_validate])

    def validate_username(self, username):

        # checking username unique
        user = get_user_model().objects.filter(phone_number=username)
        if user.exists():
            raise serializers.ValidationError("User with this phone_number already exists.")

        return username
    
    @classmethod
    def check_limit(cls, request):
        """
        Checking limit for ip address
        """
        ip_address = request.META.get('REMOTE_ADDR')

        limit = cache.get(ip_address, 0)
        if limit >= 3:
            raise serializers.ValidationError('Try after one hour')
        else:
            cache.set(ip_address, limit + 1, 60 * 60)

    def save(self, *args, **kwargs):
        """
        Send registration code to phone number user.
        """
        self.check_limit(self.context['request'])

        code = EskizUz.send_sms(
            send_type='AUTH_CODE',
            username=self.validated_data['username'],
            )

        self.validated_data['code'] = code


class VerifyCodeSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.IntegerField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        username, code = attrs['username'], attrs['code']

        if cache.get(EskizUz.AUTH_CODE_KEY.format(username=username)) != code:
            raise serializers.ValidationError('Invalid verify code or username')

        return attrs
    

class RegisterSerializer(VerifyCodeSerializer):
    fullname = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128, validators=[validate_password], write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        username, password, fullname = attrs['username'], attrs['password'], attrs['fullname']

        user = get_user_model().objects.create_user(phone_number=username, fullname=fullname, password=password)
        
        cache.delete(EskizUz.AUTH_CODE_KEY.format(username=username))

        tokens = generate_jwt_tokens(user)

        attrs = {**attrs, **tokens}

        attrs['role'] = user.role

        return attrs