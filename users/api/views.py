from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from .serializers import RegisterUserSerializer, LoginSerializer, VerifyTokenSerializer
from rest_framework.response import Response
from rest_framework import status

class RegisterUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = RegisterUserSerializer

class VerifyEmailView(APIView):
    """Verify a user email"""
    serializer_class = VerifyTokenSerializer
    def post(self, request, format=None):
        token = request.data.get('token')
        try :
            user = get_user_model().objects.get(verify_token=token)
            user.email_verified = True
            user.save()
        except Exception as e:
            return Response('Invalid token', status=status.HTTP_400_BAD_REQUEST)
        return Response(RegisterUserSerializer(user).data, status=status.HTTP_200_OK)
        

class LoginView(ObtainAuthToken):
    """Create a new auth token for the user"""
    serializer_class = LoginSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
