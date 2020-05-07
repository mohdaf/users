from django.urls import path, include
from .views import RegisterUserView, LoginView, VerifyEmailView, ChangePasswordView, UserViewSet

from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'', UserViewSet)

app_name = 'users'

urlpatterns = [
    path('users/', include(router.urls), name='users'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]