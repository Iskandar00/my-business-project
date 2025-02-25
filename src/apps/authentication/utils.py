from rest_framework_simplejwt.tokens import RefreshToken


def generate_jwt_tokens(user):
    refresh = RefreshToken.for_user(user)
    refresh['role'] = user.role
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }