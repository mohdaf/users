from django.urls import path, include
from .views import RegisterUserView, LoginView, VerifyEmailView, ChangePasswordView

from rest_framework.routers import DefaultRouter

app_name = 'users'

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]