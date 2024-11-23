from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from passwords.models import User
from passwords.serializers import LoginSerializer
from google.oauth2 import id_token
from google.auth.transport import requests

from passwords.settings import GOOGLE_CLIENT_ID


def validate_token(token):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

        userid = idinfo['sub']

        return idinfo
    except ValueError:
        return None


def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})


class ProtectedView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to Password API',
        })

class SignUpView(APIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        # Validate the input data
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract the token and cookies
        user_token = serializer.validated_data["token"]

        # Validate the token via an external API
        user_data = validate_token(user_token)

        if not user_data:
            return Response(
                {"detail": "Invalid token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Retrieve or create a user based on the external API response
        user = User.objects.create(
            email=user_data["email"],
            google_picture=user_data["picture"],
            name=user_data["name"],
        )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        # Validate the input data
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract the token and cookies
        user_token = serializer.validated_data["token"]

        # Validate the token via an external API
        user_data = validate_token(user_token)

        if not user_data:
            return Response(
                {"detail": "Invalid token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Retrieve or create a user based on the external API response
        try:
            user = User.objects.get(
                email=user_data["email"]
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "User does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )
