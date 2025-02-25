from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

    
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = RefreshToken(attrs['refresh'])

        access = data['access']
        token = AccessToken(access)

        role = refresh.get('role')
        token['role'] = role  

        data['access'] = str(token)
        data['role'] = role
        return data