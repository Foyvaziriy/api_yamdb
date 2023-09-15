from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    username = serializers.SlugField(max_length=150)
    email = serializers.EmailField(max_length=254)


class AuthSerializer(serializers.Serializer):
    username = serializers.SlugField(max_length=150)
    confirmation_code = serializers.CharField(max_length=256)
