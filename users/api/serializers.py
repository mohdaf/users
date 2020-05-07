from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from .tokens import account_activation_token
from django.core.mail import EmailMessage


class RegisterUserSerializer(serializers.ModelSerializer):
    """Creating new users"""
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        """create new user"""
        created_user = get_user_model().objects.create_user(**validated_data)
        token = account_activation_token.make_token(created_user)
        created_user.verify_token = token
        created_user.save()
        mail_subject = 'Activate your account'
        message = token
        to_email = validated_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return created_user


class VerifyTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    token = serializers.CharField(required=True)


class LoginSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            raise serializers.ValidationError('Unable to authenticate with provided credentials', code='authorization')
        if not user.email_verified:
            raise serializers.ValidationError('Email is not verified', code='authorization')
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change."""
    password = serializers.CharField(required=True)


class AuthUserSerializer(serializers.ModelSerializer):
    """views users internally"""
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')


class PublicUserSerializer(serializers.ModelSerializer):
    """views users externally"""
    class Meta:
        model = get_user_model()
        fields = ('first_name',)
