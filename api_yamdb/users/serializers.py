from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class ConfCodeField(serializers.SlugField):
    def to_internal_value(self, data):
        if isinstance(data, bool) or not isinstance(data, (str,)):
            self.fail('invalid')
        value = str(data)
        return value.strip() if self.trim_whitespace else value


class SignUpSerializer(serializers.Serializer):
    username = serializers.SlugField(max_length=150)
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        return not value == 'me'


class AuthSerializer(serializers.Serializer):
    username = serializers.SlugField(max_length=150)
    confirmation_code = ConfCodeField(max_length=256)
