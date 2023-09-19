from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    username = serializers.SlugField(max_length=150)
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('You cant use "me" as username')
        return value


class AuthSerializer(serializers.Serializer):
    username = serializers.SlugField(max_length=150)
    confirmation_code = serializers.SlugField(max_length=256)
