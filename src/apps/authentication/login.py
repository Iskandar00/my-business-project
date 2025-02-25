from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.signals import user_logged_in

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.utils import generate_jwt_tokens

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for handling JWT token generation with phone number authentication.
    """

    role = serializers.CharField(read_only=True)

    def validate(self, attrs):
        """
        Validate the user credentials and generate JWT tokens.
        """
        username = attrs.get('phone_number')
        password = attrs.get('password')

        user = get_object_or_404(User, phone_number=username)

        if not user.check_password(password):
            raise serializers.ValidationError({"detail": _("Username or password is incorrect")}, code=404)

        if not user.is_active:
            raise serializers.ValidationError({"detail": _("User is not active")}, code=403)

        tokens = generate_jwt_tokens(user)

        user_logged_in.send(sender=user.__class__, request=self.context["request"], user=user)

        return {
            'refresh': str(tokens['refresh']),
            'access': str(tokens['access']),
            'role': user.role,
        }

    def get_token(self, user):
        token = super().get_token(user)
        token['role'] = user.role  # Добавляем роль в payload access token
        return token


class CustomTokenObtainPairView(GenericAPIView):
    """
    Custom view for handling JWT token generation requests.
    Inherits from GenericAPIView to provide token generation endpoint.

    This view processes POST requests to authenticate users and return JWT tokens.
    No authentication is required to access this endpoint (typically used for login).
    """
    # Empty permission_classes and authentication_classes means this endpoint is publicly accessible
    permission_classes = []
    authentication_classes = []

    # Specify the serializer that will handle the validation and token generation
    serializer_class = CustomTokenObtainPairSerializer

    # Empty queryset as this view doesn't need to query any models directly
    queryset = []

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for token generation.

        Args:
            request: The HTTP request object containing user credentials
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            Response: 
                - 200 OK with JWT tokens if authentication is successful
                - 400 Bad Request if validation fails

        Request body should contain:
            {
                "username": "phone_number or email",
                "password": "user_password"
            }
        """
        # Create serializer instance with the request data
        serializer = CustomTokenObtainPairSerializer(data=request.data, context={"request":request})

        # Validate the incoming data
        if serializer.is_valid():
            # Return JWT tokens if validation is successful
            return Response(serializer.validated_data, status=200)

        # Return validation errors if the data is invalid
        return Response(serializer.errors, status=400)